# linklist_py/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from . import cpp_bridge

# 页面：渲染教学页面（你可以在 templates/linklist/index.html 中实现前端）
def index(request):
    # 告知前端是否使用 C++ 后端
    context = {
        "using_cpp": cpp_bridge.using_cpp_backend()
    }
    return render(request, "linklist/index.html", context)

# ---- API endpoints (JSON) ----
@csrf_exempt
@require_POST
def api_create(request):
    """
    POST JSON: { "initial": [1,2,3] } 可选
    returns: { "id": "...", "list": [...] }
    """
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    initial = body.get("initial")
    lid = cpp_bridge.create_list(initial=initial)
    snapshot = cpp_bridge.to_list(lid)
    return JsonResponse({"id": lid, "list": snapshot})

@csrf_exempt
@require_POST
def api_destroy(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    if not lid:
        return HttpResponseBadRequest("missing id")
    ok = cpp_bridge.destroy_list(lid)
    return JsonResponse({"ok": ok})

@csrf_exempt
@require_POST
def api_insert_head(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    value = body.get("value")
    if lid is None or value is None:
        return HttpResponseBadRequest("missing id or value")
    ok = cpp_bridge.insert_head(lid, int(value))
    return JsonResponse({"ok": ok, "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_POST
def api_insert_tail(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    value = body.get("value")
    if lid is None or value is None:
        return HttpResponseBadRequest("missing id or value")
    ok = cpp_bridge.insert_tail(lid, int(value))
    return JsonResponse({"ok": ok, "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_POST
def api_insert_at(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    index = body.get("index")
    value = body.get("value")
    if lid is None or index is None or value is None:
        return HttpResponseBadRequest("missing id/index/value")
    ok = cpp_bridge.insert_at(lid, int(index), int(value))
    return JsonResponse({"ok": ok, "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_POST
def api_delete_value(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    value = body.get("value")
    if lid is None or value is None:
        return HttpResponseBadRequest("missing id/value")
    res = cpp_bridge.delete_value(lid, int(value))
    return JsonResponse({"result": int(res), "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_POST
def api_delete_at(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    index = body.get("index")
    if lid is None or index is None:
        return HttpResponseBadRequest("missing id/index")
    ok = cpp_bridge.delete_at(lid, int(index))
    return JsonResponse({"ok": ok, "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_POST
def api_reverse(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except Exception:
        body = {}
    lid = body.get("id")
    if lid is None:
        return HttpResponseBadRequest("missing id")
    ok = cpp_bridge.reverse(lid)
    return JsonResponse({"ok": ok, "list": cpp_bridge.to_list(lid)})

@csrf_exempt
@require_GET
def api_search(request):
    # Accept query params ?id=...&value=...
    lid = request.GET.get("id")
    value = request.GET.get("value")
    if not lid or value is None:
        return HttpResponseBadRequest("missing id or value")
    idx = cpp_bridge.search(lid, int(value))
    return JsonResponse({"index": idx})

@csrf_exempt
@require_GET
def api_size(request):
    lid = request.GET.get("id")
    if not lid:
        return HttpResponseBadRequest("missing id")
    s = cpp_bridge.size(lid)
    return JsonResponse({"size": s})

@csrf_exempt
@require_GET
def api_snapshot(request):
    lid = request.GET.get("id")
    if not lid:
        return HttpResponseBadRequest("missing id")
    return JsonResponse({"list": cpp_bridge.to_list(lid)})
