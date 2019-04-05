$( document ).ready(function() {

    $.get($('#root').text() + "stats", function (data, status) { $('#statnum').text(data) })

    $("#wikiSearch").collapse('show');
    $( "#hledej" ).click(function() {
        $("#map").removeClass("hidden");
        GetValues();
    });

    $('#wikiSearch').on('show.bs.collapse', function () {
        $('#item').collapse('hide')
        $('#souradnice').collapse('hide')
    })
    $('#item').on('show.bs.collapse', function () {
        $('#wikiSearch').collapse('hide')
        $('#souradnice').collapse('hide')
    })

    $('#souradnice').on('show.bs.collapse', function () {
        $('#wikiSearch').collapse('hide')
        $('#item').collapse('hide')
    })

    $('#degdec').on('show.bs.collapse', function () {
        $('#dms').collapse('hide')
    })

    $('#dms').on('show.bs.collapse', function () {
        $('#degdec').collapse('hide')
    })

});
