$( document ).ready(function() {
    
    $.get("stats", function (data, status) { $('#statnum').text(data) })

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

});