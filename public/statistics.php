<?php
shell_exec("../generateStats.sh");
header("Location: stats.html");
