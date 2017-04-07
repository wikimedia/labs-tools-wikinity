<?php
shell_exec("../visitors -A -o html --grep 'map.py' ~/access.log > stats.html");
header("Location: stats.html");
