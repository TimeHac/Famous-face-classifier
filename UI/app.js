Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "http://127.0.0.1:5000/classify_image",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Drop an image or click to upload",
        autoProcessQueue: false
    });

    dz.on("addedfile", function () {
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("sending", function (file, xhr, formData) {
        console.log("📤 Uploading:", file.name);
    });

    dz.on("success", function (file, response) {
        console.log("🎯 Classification result:", response);

        if (!response || response.length === 0) {
            $("#resultHolder").hide();
            $("#divClassTable").hide();
            $("#error").show();
            return;
        }

        let players = ["Bill_Gates", "maria_sharapova", "mark_zuckerberg", "elon_musk", "ms_dhoni"];

        let match = null;
        let bestScore = -1;
        for (let i = 0; i < response.length; ++i) {
            let maxScoreForThisClass = Math.max(...response[i].class_probability);
            if (maxScoreForThisClass > bestScore) {
                match = response[i];
                bestScore = maxScoreForThisClass;
            }
        }

        if (match) {
            $("#error").hide();
            $("#resultHolder").show();
            $("#divClassTable").show();
            $("#resultHolder").html($(`[data-player="${match.class}"`).html());
            let classProbability = match.class_probability;
            let classDict = match.class_dictionary;

            for (let [personName, index] of Object.entries(classDict)) {
                let probabilityScore = classProbability[index].toFixed(2) + "%";
                let elementId = "#score_" + personName;
                console.log("➡", elementId, "=", probabilityScore);
                $(elementId).html(probabilityScore);
                }
        }
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function () {
    console.log("✅ Ready!");
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
