# Standard Library Imports
from functools import reduce
import json

# Third-party imports
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

# Django imports    
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Local imports
from .models import JobPosting
from django.db.models import Q

import logging



# Third-party imports

# Django imports

# Application imports

# Create your views here.
ITEM_COUNT_PER_PAGE = 30
SCHEMA_FILED_EXCEPT = [
    "page",
    # "filter",
    "id",
    "count_per_page",
    "depth",
    "logic",
    "order_by",
    "ignore[]",
    "content_type",
    "prefetch",
]
CHAIN_FILTER = [
    "startswith",
    "endwith",
    "lte",
    "gte",
    "gt",
    "lt",
    "contains",
    "icontains",
    "exact",
    "iexact",
]
logger = logging.getLogger(__name__)

def getSerializer(modelClass):
    class_name = modelClass.__name__
    class ApiSerializer(serializers.ModelSerializer):
        class Meta:
            model = modelClass
            fields = "__all__"
            ref_name = f"{class_name}API"  # 고유한 ref_name 설정

    return ApiSerializer



def readQuery(request, key):
    if "[]" in key:
        value = request.GET.get(key, "[]")
        if value == "[]":
            value = [-1]
        elif value.startswith("["):
            value = json.loads(value)
        else:
            value = request.GET.getlist(key)
        key = key.replace("[]", "")
    elif key.endswith("__not"):
        k = key.replace("__not", "")
        value = request.GET.get(key)
        return ~Q(**{k: value})
    else:
        value = request.GET.get(key)
        if value == "true":
            value = True
        elif value == "false":
            value = False
    return Q(**{key: value})


def applyOption(request, queryset):
    op = request.GET.get("filter")
    logic = request.GET.get("logic")
    where = [Q()]
    where__and = [Q()]
    used_keys = []
    if logic:
        keys = logic.split("__OR__")
        for key in keys:
            used_keys.append(key)
            where.append(readQuery(request, key))
    params = {}
    for key in request.GET:
        if key in SCHEMA_FILED_EXCEPT or key in used_keys:
            continue
        if key == "filter" and op is not None:
            params = json.loads(op)
        else:
            where__and.append(readQuery(request, key))

    queryset = queryset.filter(
        reduce(lambda x, y: x | y, where),
        reduce(lambda x, y: x & y, where__and),
    ).distinct()

    if len(params) != 0:
        queryset = queryset.filter(**params).distinct()

    return queryset

def my_note(request):
            return render(request, 'my_note.html')
        
def getViewSet(modelClass):
    class ApiViewSet(viewsets.ModelViewSet):
        queryset = modelClass.objects.all().order_by("-id")
        serializer_class = getSerializer(modelClass)
        def list(self, request):
            page = request.GET.get("page")
            depth = request.GET.get("depth")
            count = request.GET.get("count_per_page")
            order = request.GET.get("order_by")
            ignore = request.GET.get("ignore[]")
            if ignore:
                ignore = request.GET.getlist("ignore[]")
            else:
                ignore = []
            queryset = applyOption(request, self.queryset)
            if order:
                queryset = queryset.order_by(*order.split(","))
            if page:
                res = applyPagination(
                    queryset, self.serializer_class, page, count, depth, ignore
                )
            else:
                res = []
                if depth:  # Deprecated
                    for item in queryset.all():
                        res.append(applyDepth(item, int(depth), ignore))
                else:
                    res = self.serializer_class(queryset, many=True).data
            return Response(res, status=status.HTTP_200_OK)

        def update(self, request, *args, **kwargs):
            partial = True
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

    return ApiViewSet


def applyPagination(queryset, serializer_class, page, count, depth, ignore):
    count_val = int(count) if count else ITEM_COUNT_PER_PAGE
    paginator = Paginator(queryset, count_val)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    output = []
    if depth:
        for item in items:
            output.append(applyDepth(item, int(depth), ignore))
    else:
        output = serializer_class(items, many=True).data
    res = {
        "items": output,
        "total_page": paginator.num_pages,
        "total": paginator.count,
    }
    return res


def applyDepth(item, depth, ignore):
    if item is None:
        return None
    if depth == -1:
        return item.id
    data = getSerializer(item.__class__)(item).data
    for field in item.__class__._meta.get_fields():
        if field.name in ignore:
            continue
        if field.many_to_one or field.one_to_one:
            if not hasattr(item, field.name):
                continue
            data[field.name] = applyDepth(getattr(item, field.name), depth - 1, ignore)
        elif field.many_to_many:
            if not hasattr(item, field.name):
                continue
            data[field.name] = []
            for m2m_item in getattr(item, field.name).all():
                data[field.name].append(applyDepth(m2m_item, depth - 1, ignore))
    return data

def search_job_postings(country=None, task_code=None):
    queryset = JobPosting.objects.all()

    if country:
        queryset = queryset.filter(country=country)

    if task_code:
        queryset = queryset.filter(tasks__code=task_code)

    return queryset

def match_profiles(profile1, profile2):
    if not profile1.matched_with and not profile2.matched_with:
        profile1.matched_with = profile2.user
        profile2.matched_with = profile1.user
        profile1.save()
        profile2.save()

