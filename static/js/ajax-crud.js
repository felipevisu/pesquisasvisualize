$(function () {
    $("body").on("click", ".js-btn", function() {
        var btn = $(this);
        var url = btn.attr("data-url") + window.location.search
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $(".modal .modal-content").html('<div class="modal-body p-3 text-center">Carregando...</div>');
                $(".modal").modal("show");
            },
            success: function (data) {
                $(".modal .modal-content").html(data.chart);
            }
        });
    });
});