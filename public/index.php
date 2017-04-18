<?php
// Force HTTPS for our users
if (getallheaders()['X-Forwarded-Proto'] == "http") {
	header("Location: https://".$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']);
}
require_once __DIR__ . '/../vendor/autoload.php';
$I18N = new Intuition( 'wikinity' );
$I18N->registerDomain( 'wikinity', __DIR__ . '/../messages' );
?>
<!DOCTYPE HTML>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Wikinity</title>
  <!-- font awesome -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <!-- Latest compiled and minified JavaScript -->
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  <style>
    .hidden {
        display: none !important;
        visibility: hidden !important;
    }

    .stat {
        font-family: "Times New Roman", Times, serif;
        font-size:150%;
        text-decoration:underline;
    }
  </style>
</head>
<body>

  <!-- navbar -->
  <nav class="navbar navbar-inverse bg-faded" style="background-color:#337ab7;border-color: 2e6da4">
      <a class="navbar-brand" href="#" style="color: #fff"> 
        Wikinity
      </a>
      <a class="navbar-brand" href="https://github.com/urbanecm/wikinity/" style="color: #fff;float: right">
          <i class="fa fa-github fa-lg" aria-hidden="true"></i> GitHub - zdrojový kód
      </a>
      <ul class="nav navbar-nav" style="float: right">
      <li>
      <form>
      <select class="selectpicker">
      <?php
      $langs = $I18N->getAvailableLangs();
      foreach ($langs as $key => $value)
      {
	      $toEcho = "";
	      if ($key == $I18N->getLang())
	      {
		      $toEcho = '<option selected value="' . $key . '">' . $value . '</option>';
	      }
	      else
	      {
		      $toEcho = '<option value="' . $key . '">' . $value . '</option>';
	      }
	      echo( $toEcho );
      }
      ?>
      </select>
      </form>
      </li>
      <li><a style="color: #fff" href="https://github.com/urbanecm/wikinity/issues/new">Nahlásit problém</a></li>
      </ul>
  </nav>
  
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
          </div>
      </div>
  </div>
 
<script>

    
    function GetValues() {

        var serialized;
        var wikiSearch = $("#wikiSearchPole").val();
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
        $( "#stat" ).load( "https://tools.wmflabs.org/wikinity/stats.py p#stat" );
        $("#wikiSearch").collapse('show');
        $( "#hledej" ).click(function() {
            $( "#stat" ).load( "https://tools.wmflabs.org/wikinity/stats.py p#stat" );
            $("#map").removeClass("hidden");
            GetValues();
        });

        $('#wikiSearch').on('show.bs.collapse', function () {
            $('#item').collapse('hide')
        })
        $('#item').on('show.bs.collapse', function () {
            $('#souradnice').collapse('hide')
        })

        $('#souradnice').on('show.bs.collapse', function () {
            $('#item').collapse('hide')
        })

    });
</script>
</body>
</html>
