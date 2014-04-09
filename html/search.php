<?php
	
	header('Content-Type: application/json');
	chdir('../');
	
	if (isset($_POST['q']) && $_POST['q'] != '') {
		$query = strtoupper(str_replace('"', '\\"', preg_replace(' {2,}', ' ', preg_replace('(AND|-)', ' ', $_POST['q']))));
		if (isset($_POST['action']) && $_POST['action'] == 'search') {
			echo shell_exec('python searchEngine.py -j "'.$query.'"');
			return;
		}
		else if(isset($_POST['action']) && $_POST['action'] == 'expand' && isset($_POST['file'])) {
			$file = preg_replace('(\.|\\|\/)', '', $_POST['file']);
			$contents = file_get_contents('../documents/'.$file);
			
		}
	}
	echo '{}';
