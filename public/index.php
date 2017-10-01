<?php include 'header.php'; ?>
<body>

<?php include 'navbar.php'; ?>
<!-- Forms -->
  <div class="container">
    <form>
      <div class="row">
          <div class="col">
            <div class="radio">
                <label><input type="radio" name="optradio" data-toggle="collapse" data-target="#wikiSearch" checked><?php echo $I18N->msg("enter-name-of-article"); ?></label>
            </div>
          </div>
        <div class="col collapse" id="wikiSearch">
          <div class="form-group">
              <input type="text" class="form-control" name="wikiSearchPole" id="wikiSearchPole" placeholder="<?php echo $I18N->msg("prague"); ?>, (<?php echo $I18N->msg("default-value");?>)">
          </div>
        </div>
          <div class="col">
            <div class="radio">
                <label><input type="radio" name="optradio" data-toggle="collapse" data-target="#item"><?php echo $I18N->msg("enter-number-of-item"); ?></label>
            </div>
          </div>
        <div class="col collapse" id="item">
          <div class="form-group">
              <input type="text" class="form-control" name="cislo" id="cislo" placeholder="Q1085 (<?php echo $I18N->msg("prague"); ?>, <?php echo $I18N->msg("default-value");?>)">
          </div>
        </div>
        <div class="radio">
            <label><input type="radio" name="optradio" data-toggle="collapse" data-target="#souradnice"><?php echo $I18N->msg("enter-coordinates");?></label>
        </div>
        <div class="col collapse" id="souradnice">
          <div id="error2" class="alert alert-danger fade in hidden">
              <a href="#" class="close" data-dismiss="alert">&times;</a>
              <strong>Error!</strong> pole souradnice je povinne.
          </div>
          <div class="form-group">
              <label for="formGroupExampleInput">Souřadnice lat</label>
              <input id="lat" type="text" name="lat" class="form-control" id="formGroupExampleInput" placeholder="50.088611 (<?php echo $I18N->msg("prague"); ?>, <?php echo $I18N->msg("default-value");?>)">
          </div>
          <div class="form-group">
              <label for="formGroupExampleInput2">Souřadnice lon</label>
              <input id="lon" type="text" name="lon" class="form-control" id="formGroupExampleInput2" placeholder="14.421389 (<?php echo $I18N->msg("prague"); ?>, <?php echo $I18N->msg("default-value");?>)">
          </div>
        </div>
        <div class="col">
            <label><?php echo $I18N->msg("select-displayed"); ?></label>
        </div>
        <div class="col">
          <input id="nafocene" type="checkbox" name="check" value="nafoceno">
          <label for="ch1"><?php echo $I18N->msg("photographed");?></label>
        </div>
        <div class="col">
          <input id="nenafocene" type="checkbox" name="check" value="nenafoceno" checked>
          <label for="ch2"><?php echo $I18N->msg("unphotographed");?></label>
        </div>
        <div class="col">
          <div class="form-group">
              <label for="formGroupExampleInput"><?php echo $I18N->msg("enter-radius"); ?></label>
              <input id="radius" type="text" name="radius" class="form-control" id="formGroupExampleInput" placeholder="5 (<?php echo $I18N->msg("default-value");?>)">
          </div>
        </div>
        <div class="col-3">
              <button type="button" class="btn btn-primary" id="hledej"><?php echo $I18N->msg("search");?></button>
        </div>

      </div>
    </form>
  </div>

  <div class="container">
      <div class="row">
          <div class="col" id="map" style="padding-top:2.5%; width:70%">
            <!--<div class="embed-responsive embed-responsive-16by9">
                <iframe id="map" class="embed-responsive-item hidden" src=""></iframe>
            </div>-->
          </div>
          <div class="col" id="stat">
			  <p>Tento nástroj vygeneroval již <span id="statnum"></span> map.</p>
          </div>
      </div>
  </div>

<script>


    function GetValues() {

        var serialized;
        var wikiSearch = $("#wikiSearchPole").val().replace(/ /g, '_');
        var item = $("#cislo").val();
        var lat = $("#lat").val();
        if (wikiSearch != "")
        {
            serialized = '?' + 'type=article' + '&article=' + wikiSearch;
        }
        else if(item != "")
        {
            serialized = '?' + 'type=item' + '&item=' + item;
        }else if(lat != "")
        {
            serialized = '?' + 'type=coor' + '&lat=' + $("#lat").val() + '&lon=' + $("#lon").val();
        }else {
            serialized = '?' + 'type=item' + '&item=' + "Q1085";
        }
        var nafoceno = $('#nafocene').is(':checked');
        var nenafoceno = $('#nenafocene').is(':checked');
        //check if all checkbox are checked
        if(nafoceno == true && nenafoceno == true)
        {
            serialized += '&' + 'subtype=all';
        }else if(nafoceno == true)
        {
            serialized += '&' + 'subtype=nafoceno';
        }else if(nenafoceno == true)
        {
            serialized += '&' + 'subtype=nenafoceno';
        }
        else {
            serialized += '&' + 'subtype=nenafoceno';
        }

        if($("#radius").val() != "") {
            serialized += '&' + 'radius=' + $("#radius").val();
        }
        else {
            serialized += '&' + 'radius=' + "5";
        }

        //debug
        console.log(serialized);
        //document.getElementById('map').setAttribute('src', "https://tools.wmflabs.org/wikinity/map.py" + serialized);
        var addr = "https://tools.wmflabs.org/wikinity/map.py" + serialized;
        console.log(addr);
        $('#map').load(addr, "#map");
    }

    $( "select" ).on( "change", GetValues );

    $( document ).ready(function() {
        $( "#statnum" ).load( "https://tools.wmflabs.org/wikinity/stats.py p#statnum" );
        $("#wikiSearch").collapse('show');
        $( "#hledej" ).click(function() {
            $( "#statnum" ).load( "https://tools.wmflabs.org/wikinity/stats.py p#statnum" );
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
</script>
</body>
</html>
