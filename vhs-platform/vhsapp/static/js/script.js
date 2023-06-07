function to_manifest(witnessRef, version) {
    const witnessType = witnessRef.startsWith(MS_ABBR) ? MS.toLowerCase() : VOL.toLowerCase()
    return `${VHS_APP_URL}/${APP_NAME}/iiif/${version}/${witnessType}/${formatWitRef(witnessRef)}/manifest.json`
}

function extractNb(str) {
    return str.match(/\d+/g).toString();
}

function formatWitRef(witnessRef, onlyId= false){
    if (onlyId){
        return extractNb(witnessRef);
    }

    if (witnessRef.includes("-")){
        return witnessRef;
    }
    return witnessRef.replace(/([a-zA-Z])(\d+)/g, "$1-$2");
}

function getJSON(url, callback, idMessage) {
    fetch(url).then(response => {
        if (response.ok) { return response.json(); }
        throw new Error(`Failed to load ${url} due to ${response.status}: ${response.statusText}`);
    }).then(response => {
        callback(response.status, response);
    }).catch(error => {
        showMessage(error.message, idMessage);
    });
}

function editAnnotations(witnessRef, idButton) {
    /* Function triggered on click on the "v2" btn that redirects to the show page to correct annotations */
    const manifestUrl = to_manifest(witnessRef, "auto");
    const idMessage = `message_${extractNb(witnessRef)}`;
    const witnessType = new URL(manifestUrl).pathname.split("/")[4];
    const innerHtml = $(`#${idButton}`).html();

    setLoading(idButton);

    function populate_annotations(status, data, idMessage) {
        fetch(`${SAS_APP_URL}/manifests`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`Failed to index ${data["@id"]} due to ${response.status}: ${response.statusText}`);
            }

            fetch(`/${APP_NAME}/iiif/v2/${witnessType}/${formatWitRef(witnessRef, true)}/populate/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to load and display annotations for ${witnessRef} due to ${response.status}: ${response.statusText}`);
                    }
                    window.open(`/${APP_NAME}/${witnessType}/${formatWitRef(witnessRef, true)}/show/`, "_blank");
                    clearLoading(idButton, innerHtml)
                })
                .catch(error => {
                    showMessage(error.message, idMessage);
                });
        }).catch(error => {
            showMessage(error.message, idMessage);
        });
    }

    fetch(manifestUrl).then(response => {
        // first check if the manifest is correct
        if (response.ok) { return response.json(); }
        throw new Error(`Failed to load ${url} due to ${response.status}: ${response.statusText}`);
    }).then(response => {
        // second, launch indexing of annotations
        populate_annotations(response.status, response, idMessage);
    }).catch(error => {
        showMessage(error.message, idMessage);
    });
}


function finalAnnotations(btn) {
    /* Function triggered on click on the "final" btn that redirects to the show page to correct annotations */
    const idButton = btn.attr("id");
    const innerHtml = btn.html()
    const witnessRef = idButton.split("_").pop();
    setLoading(idButton);
    window.open(`${SAS_APP_URL}/indexView.html?iiif-content=${to_manifest(witnessRef, "v2")}`, "_blank");
    clearLoading(idButton, innerHtml);
    return false;
}


function viewAnnotations(witnessRef) {
    /* Function triggered on click on the "auto" btn that redirects to a Mirador viewer */
    const manifestUrl = to_manifest(witnessRef, "auto");
    const idMessage = `message_auto_${extractNb(witnessRef)}`;

    fetch(manifestUrl).then(response => {
        if (response.ok) {
            window.open(`${SAS_APP_URL}/indexAnnos.html?iiif-content=${manifestUrl}`, "_blank");
        } else {
            showMessage(`Failed to load ${manifestUrl} due to ${response.status}: ${response.statusText}`, idMessage);
        }
    }).catch(error => {
        showMessage(`Failed to load ${manifestUrl}: ${error.message}`, idMessage);
    });
}

function showMessage(message, idMessage) {
    const msgElement = document.getElementById(idMessage);
    if (msgElement) {
        msgElement.textContent = message;
        msgElement.style.display = "block";
    }
}

function setLoading(idButton) {
    const button = document.getElementById(idButton);
    button.innerHTML = "<span class='fa fa-spinner fa-spin fa-pulse fa-1x'></span> Indexing...";
    button.disabled = true;
}

function clearLoading(idButton, innerHtml) {
    const button = document.getElementById(idButton);
    button.innerHTML = innerHtml;
    button.disabled = false;
}

function deleteAnnotation(annoId) {
    const HTTP_SAS = SAS_APP_URL.replace("https", "http");
    const urlDelete = `${SAS_APP_URL}/annotation/destroy?uri=${HTTP_SAS}/annotation/${annoId}`;

    fetch(urlDelete, {
        method: "DELETE"
    }).then(response => {
        if (response.status === 204) {
            const annoDiv = $(`#ill_${annoId}`).closest("div");
            annoDiv.fadeOut(function() { annoDiv.remove() });
        } else {
            showMessage(`Failed to delete ${urlDelete} due to ${response.status}: '${response.statusText}'`, `message_${annoId}`);
        }
    }).catch(error => {
        showMessage(`Failed to delete ${urlDelete}: ${error.message}`, `message_${annoId}`);
    });
}

function deleteAnnotations(annoIds){
    if (annoIds.length > 0) {
        if (confirm(APP_LANG === "en" ? "Are you sure you want to delete corresponding annotations?"
            : "Êtes-vous sûr de vouloir supprimer les annotations sélectionnées ?")) {
            for (let i = 0; i < annoIds.length; i++) {
                deleteAnnotation(annoIds[i]);
            }
            return true;
        }
        return false;
    }
    alert(APP_LANG === "en" ? "Please select at least one annotation to delete" : "Veuillez sélectionner au moins une image à supprimer.");
    return false;
}

function deleteAllAnnotations(allAnnos) {
    if (confirm(APP_LANG === "en" ? "Are you sure you want to delete all annotations?"
        : "Êtes-vous sûr de vouloir supprimer toutes les annotations ?")) {
        for (let i = allAnnos.length - 1; i >= 0; i--) {
            deleteAnnotation(allAnnos[i]);
        }
    }
}
