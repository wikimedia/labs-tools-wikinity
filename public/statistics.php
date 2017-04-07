<?php
echo(shell_exec("../visitors -A -o html --grep 'map.py' ~/access.log 2>/dev/null"));
