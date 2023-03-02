from rest_framework import generics
from django_filters.rest_framework import CharFilter, UUIDFilter, NumberFilter
from django.db.models import Count


from alyx.base import BaseFilterSet, rest_permission_classes
from experiments.models import (ProbeInsertion, TrajectoryEstimate, Channel, BrainRegion,
                                ChronicInsertion)
from experiments.serializers import (ProbeInsertionListSerializer, ProbeInsertionDetailSerializer,
                                     TrajectoryEstimateSerializer, ChannelSerializer,
                                     BrainRegionSerializer, ChronicInsertionDetailSerializer,
                                     ChronicInsertionListSerializer)

"""
Probe insertion objects REST filters and views
"""


def _filter_qs_with_brain_regions(self, queryset, region_field, region_value):
    brs = BrainRegion.objects.filter(
        **{region_field: region_value}).get_descendants(include_self=True)
    qs_trajs = TrajectoryEstimate.objects.filter(provenance__gte=70). \
        prefetch_related('channels__brain_region'). \
        filter(channels__brain_region__in=brs).distinct()
    if queryset.model.__name__ == 'Session':
        qs = queryset.prefetch_related('probe_insertion__trajectory_estimate').filter(
            probe_insertion__trajectory_estimate__in=qs_trajs)
    elif (queryset.model.__name__ == 'ProbeInsertion' or
          queryset.model.__name__ == 'ChronicInsertion'):
        qs = queryset.prefetch_related('trajectory_estimate').filter(
            trajectory_estimate__in=qs_trajs)
    return qs


class ProbeInsertionFilter(BaseFilterSet):
    subject = CharFilter('session__subject__nickname')
    date = CharFilter('session__start_time__date')
    experiment_number = CharFilter('session__number')
    name = CharFilter('name')
    session = UUIDFilter('session')
    model = CharFilter('model__name')
    dataset_types = CharFilter(field_name='dataset_types', method='filter_dataset_types')
    datasets = CharFilter(field_name='datasets', method='filter_datasets')
    lab = CharFilter(field_name='session__lab__name', lookup_expr='iexact')
    project = CharFilter(field_name='session__project__name', lookup_expr='icontains')
    task_protocol = CharFilter(field_name='session__task_protocol', lookup_expr='icontains')
    tag = CharFilter(field_name='tag', method='filter_tag')
    # brain region filters
    atlas_name = CharFilter(field_name='name__icontains', method='atlas')
    atlas_acronym = CharFilter(field_name='acronym__iexact', method='atlas')
    atlas_id = NumberFilter(field_name='pk', method='atlas')

    def filter_tag(self, queryset, _, value):
        """
        returns insertions that contain datasets tagged as
        :param queryset:
        :param name:
        :param value:
        :return:
        """
        queryset = queryset.filter(
            datasets__tags__name__icontains=value).distinct()
        return queryset

    def atlas(self, queryset, name, value):
        """
        returns sessions containing at least one channel in the given brain region.
        Hierarchical tree search"
        """
        return _filter_qs_with_brain_regions(self, queryset, name, value)

    def filter_dataset_types(self, queryset, _, value):

        dtypes = value.split(',')
        queryset = queryset.filter(datasets__dataset_type__name__in=dtypes)
        queryset = queryset.annotate(
            dtypes_count=Count('datasets__dataset_type', distinct=True))
        queryset = queryset.filter(dtypes_count__gte=len(dtypes))
        return queryset

    def filter_datasets(self, queryset, _, value):
        dsets = value.split(',')
        queryset = queryset.filter(datasets__name__in=dsets)
        queryset = queryset.annotate(
            dsets_count=Count('datasets', distinct=True))
        queryset = queryset.filter(dsets_count__gte=len(dsets))
        return queryset

    class Meta:
        model = ProbeInsertion
        exclude = ['json']


class ProbeInsertionList(generics.ListCreateAPIView):
    """
    get: **FILTERS**

    -   **name**: probe insertion name `/trajectories?name=probe00`
    -   **subject**: subject nickname: `/insertions?subject=Algernon`
    -   **date**: session date: `/inssertions?date=2020-01-15`
    -   **experiment_number**: session number `/insertions?experiment_number=1`
    -   **session**: session UUID`/insertions?session=aad23144-0e52-4eac-80c5-c4ee2decb198`
    -   **task_protocol** (icontains)
    -   **location**: location name (icontains)
    -   **project**: project name (icontains)
    -   **model**: probe model name `/insertions?model=3A`
    -   **lab**: lab name (exact)
    -   **tag**: tag name (icontains)
    -   **dataset_types**: dataset type(s)
    -   **datasets**: datasets name(s)
    -   **atlas_name**: returns a session if any channel name icontains
     the value: `/insertions?brain_region=visual cortex`
    -   **atlas_acronym**: returns a session if any of its channels name exactly
     matches the value `/insertions?atlas_acronym=SSp-m4`, cf Allen CCFv2017
    -   **atlas_id**: returns a session if any of its channels id matches the
     provided value: `/insertions?atlas_id=950`, cf Allen CCFv2017

    [===> probe insertion model reference](/admin/doc/models/experiments.probeinsertion)
    """
    queryset = ProbeInsertion.objects.all()
    queryset = ProbeInsertionListSerializer.setup_eager_loading(queryset)
    serializer_class = ProbeInsertionListSerializer
    permission_classes = rest_permission_classes()
    filter_class = ProbeInsertionFilter


class ProbeInsertionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProbeInsertion.objects.all()
    serializer_class = ProbeInsertionDetailSerializer
    permission_classes = rest_permission_classes()


class ChronicInsertionFilter(BaseFilterSet):
    subject = CharFilter('subject__nickname')
    lab = CharFilter('lab__name')
    model = CharFilter('model__name')
    probe = UUIDFilter('probe_insertion__id')
    session = UUIDFilter('probe_insertion__session__id')
    serial = CharFilter('serial')

    # brain region filters
    atlas_name = CharFilter(field_name='name__icontains', method='atlas')
    atlas_acronym = CharFilter(field_name='acronym__iexact', method='atlas')
    atlas_id = NumberFilter(field_name='pk', method='atlas')

    def atlas(self, queryset, name, value):
        """
        returns sessions containing at least one channel in the given brain region.
        Hierarchical tree search"
        """
        return _filter_qs_with_brain_regions(self, queryset, name, value)

    class Meta:
        model = ChronicInsertion
        exclude = ['json']


class ChronicInsertionList(generics.ListCreateAPIView):
    """
    get: **FILTERS**

    -   **name**: chronic insertion name `/chronic-insertions?name=probe00`
    -   **subject**: subject nickname: `/chronic-insertions?subject=Algernon`
    -   **lab**: lab name `/chronic-insertions?lab=UCLA`
    -   **model**: probe model name `/insertions?model=3A`
    -   **probe**: probe UUID
    `/chronic-insertions?probe=aad23144-0e52-4eac-80c5-c4ee2decb198`
    -   **session**: session UUID
    `/chronic-insertions?session=aad23144-0e52-4eac-80c5-c4ee2decb198`
    -   **serial**: serial no. of probe `/chronic-insertions?serial=101010`
    -   **atlas_name**: returns a session if any channel name icontains
     the value: `/chronic-insertions?brain_region=visual cortex`
    -   **atlas_acronym**: returns a session if any of its channels name exactly
     matches the value `/chronic-insertions?atlas_acronym=SSp-m4`, cf Allen CCFv2017
    -   **atlas_id**: returns a session if any of its channels id matches the
     provided value: `/chronic-insertions?atlas_id=950`, cf Allen CCFv2017

    [===> chronic insertion model reference](/admin/doc/models/experiments.chronicinsertion)
    """
    queryset = ChronicInsertion.objects.all()
    queryset = ChronicInsertionListSerializer.setup_eager_loading(queryset)
    serializer_class = ChronicInsertionListSerializer
    permission_classes = rest_permission_classes()
    filter_class = ChronicInsertionFilter


class ChronicInsertionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChronicInsertion.objects.all()
    serializer_class = ChronicInsertionDetailSerializer
    permission_classes = rest_permission_classes()


"""
Trajectory Estimates objects REST filters and views
"""


class TrajectoryEstimateFilter(BaseFilterSet):
    provenance = CharFilter(method='enum_field_filter')
    subject = CharFilter('probe_insertion__session__subject__nickname')
    project = CharFilter('probe_insertion__session__projects__name')
    date = CharFilter('probe_insertion__session__start_time__date')
    experiment_number = CharFilter('probe_insertion__session__number')
    session = UUIDFilter('probe_insertion__session__id')
    probe = CharFilter('probe_insertion__name')

    class Meta:
        model = TrajectoryEstimate
        exclude = ['json']


class TrajectoryEstimateList(generics.ListCreateAPIView):
    """
    get: **FILTERS**

    -   **provenance**: probe insertion provenance
        must one of the strings among those choices:
        'Ephys aligned histology track', 'Histology track', 'Micro-manipulator', 'Planned'
        `/trajectories?provenance=Planned`
    -   **subject: subject nickname: `/trajectories?subject=Algernon`
    -   **date**: session date: `/trajectories?date=2020-01-15`
    -   **experiment_number**: session number `/trajectories?experiment_number=1`
    -   **session**: `/trajectories?session=aad23144-0e52-4eac-80c5-c4ee2decb198`
    -   **probe**: probe_insertion name `/trajectories?probe=probe01`

    [===> trajectory model reference](/admin/doc/models/experiments.trajectoryestimate)
    """
    queryset = TrajectoryEstimate.objects.all()
    serializer_class = TrajectoryEstimateSerializer
    permission_classes = rest_permission_classes()
    filter_class = TrajectoryEstimateFilter


class TrajectoryEstimateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrajectoryEstimate.objects.all()
    serializer_class = TrajectoryEstimateSerializer
    permission_classes = rest_permission_classes()


class ChannelFilter(BaseFilterSet):
    session = UUIDFilter('trajectory_estimate__probe_insertion__session')
    probe_insertion = UUIDFilter('trajectory_estimate__probe_insertion')
    subject = CharFilter('trajectory_estimate__probe_insertion__session__subject__nickname')
    lab = CharFilter('trajectory_estimate__probe_insertion__session__lab__name')

    class Meta:
        model = Channel
        exclude = ['json']


class ChannelList(generics.ListCreateAPIView):
    """
    get: **FILTERS**

    -   **subject**: subject nickname: `/channels?subject=Algernon`
    -   **session**: UUID `/channels?session=aad23144-0e52-4eac-80c5-c4ee2decb198`
    -   **lab**: lab name `/channels?lab=wittenlab`
    -   **probe_insertion**: UUID  `/channels?probe_insertion=aad23144-0e52-4eac-80c5-c4ee2decb198`

    [===> channel model reference](/admin/doc/models/experiments.channel)
    """

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(generics.ListCreateAPIView, self).get_serializer(*args, **kwargs)

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = rest_permission_classes()
    filter_class = ChannelFilter


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = rest_permission_classes()


class BrainRegionFilter(BaseFilterSet):
    acronym = CharFilter(lookup_expr='iexact')
    description = CharFilter(lookup_expr='icontains')
    name = CharFilter(lookup_expr='icontains')
    ancestors = CharFilter(field_name='ancestors', method='filter_ancestors')
    descendants = CharFilter(field_name='descendants', method='filter_descendants')

    class Meta:
        model = BrainRegion
        fields = ('id', 'acronym', 'description', 'name', 'parent')

    def filter_descendants(self, queryset, _, pk):
        r = BrainRegion.objects.get(pk=pk) if pk.isdigit() else BrainRegion.objects.get(acronym=pk)
        return r.get_descendants(include_self=True).exclude(id=0)

    def filter_ancestors(self, queryset, _, pk):
        r = BrainRegion.objects.get(pk=pk) if pk.isdigit() else BrainRegion.objects.get(acronym=pk)
        return r.get_ancestors(include_self=True).exclude(pk=0)


class BrainRegionList(generics.ListAPIView):
    """
    get: **FILTERS**

    -   **id**: Allen primary key: `/brain-regions?id=687`
    -   **acronym**: iexact on acronym `/brain-regions?acronym=RSPv5`
    -   **name**: icontains on name `/brain-regions?name=retrosplenial`
    -   **description**: icontains on description `/brain-regions?description=RSPv5`
    -   **parent**: get child nodes `/brain-regions?parent=315`
    -   **ancestors**: get all ancestors for a given ID
    -   **descendants**: get all descendants for a given ID

    [===> brain region model reference](/admin/doc/models/experiments.brainregion)
    """
    queryset = BrainRegion.objects.all()
    serializer_class = BrainRegionSerializer
    permission_classes = rest_permission_classes()
    filter_class = BrainRegionFilter


class BrainRegionDetail(generics.RetrieveUpdateAPIView):
    queryset = BrainRegion.objects.all()
    serializer_class = BrainRegionSerializer
    permission_classes = rest_permission_classes()
