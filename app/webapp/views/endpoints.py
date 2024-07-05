import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from app.webapp.models.digitization import Digitization
from app.webapp.models.regions import Regions
from app.webapp.models.witness import Witness
from app.webapp.utils.iiif.annotation import (
    get_regions_annotations,
    delete_regions as del_regions,
)
from app.webapp.utils.logger import log
from app.webapp.utils.regions import create_empty_regions

"""
VIEWS THAT SERVE AS ENDPOINTS
ONLY FOR API CALLS
"""


@csrf_exempt
def save_document_set(request):
    """
    Endpoint used to create/update a document set
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            witness_ids = data.get("witness_ids", [])
            series_ids = data.get("series_ids", [])
            regions_ids = data.get("regions_ids", [])

            # TODO create logic for saving document set etc.

            if len(witness_ids) + len(series_ids) + len(regions_ids) == 0:
                return JsonResponse(
                    {"error": "No documents to save in the set"}, status=400
                )
            return JsonResponse({"message": "Document set saved successfully"})
        except Exception as e:
            return JsonResponse({"message": "Error saving score files"}, status=500)
    return JsonResponse({"message": "Invalid request"}, status=400)


def get_canvas_regions(request, wid, rid):
    regions = get_object_or_404(Regions, id=rid)
    p_nb = int(request.GET.get("p", 0))
    if p_nb > 0:
        p_len = 50
        max_c = (
            p_nb * p_len
        )  # TODO limit to not exceed number of canvases of the witness
        min_c = max_c - p_len
        return JsonResponse(
            get_regions_annotations(
                regions, as_json=True, r_annos={}, min_c=min_c, max_c=max_c
            ),
            safe=False,
        )

    return JsonResponse(
        get_regions_annotations(regions, as_json=True),
        safe=False,
    )


def get_canvas_witness_regions(request, wid):
    witness = get_object_or_404(Witness, id=wid)
    p_nb = int(request.GET.get("p", 0))
    if p_nb > 0:
        p_len = 50
        anno_regions = {}
        max_c = (
            p_nb * p_len
        )  # TODO limit to not exceed number of canvases of the witness
        min_c = max_c - p_len
        for regions in witness.get_regions():
            anno_regions = get_regions_annotations(
                regions, as_json=True, r_annos=anno_regions, min_c=min_c, max_c=max_c
            )
    else:
        anno_regions = {}
        for regions in witness.get_regions():
            anno_regions = get_regions_annotations(
                regions, as_json=True, r_annos=anno_regions
            )

    return JsonResponse(anno_regions, safe=False)


def create_manual_regions(request, wid, did=None, rid=None):
    if request.method == "POST":
        if rid:
            regions = get_object_or_404(Regions, id=rid)
            return JsonResponse(
                {
                    "regions_id": regions.id,
                    "mirador_url": regions.gen_mirador_url(),
                },
            )

        witness = get_object_or_404(Witness, id=wid)
        digit = None
        if did:
            digit = get_object_or_404(Digitization, id=did)
        else:
            for d in witness.get_digits():
                if d.has_images():
                    digit = d
                    break

        if not digit:
            return JsonResponse(
                {"error": "No digitization available for this witness"}, status=500
            )

        regions = create_empty_regions(digit)
        if not regions:
            return JsonResponse({"error": "Unable to create regions"}, status=500)
        return JsonResponse(
            {
                "regions_id": regions.id,
                "mirador_url": regions.gen_mirador_url(),
            },
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_regions(request, rid):
    if request.method == "DELETE":
        regions = get_object_or_404(Regions, id=rid)
        try:
            del_regions(regions)
            return JsonResponse({"message": "Regions deleted"}, status=204)
        except Exception as e:
            log(f"[delete_regions] Error deleting regions #{rid}", e)
            return JsonResponse({"error": f"Error deleting regions: {e}"}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)
