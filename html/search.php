<?php
	chdir('../');
	
	if (isset($_POST['q']) && $_POST['q'] != '') {
		if(isset($_POST['action']) && $_POST['action'] == 'expand' && isset($_POST['doc'])) {
			$doc = 'documents/' . preg_replace('(\.|\\|\/)', '', $_POST['doc']);
			echo '<html>' . $doc . (file_exists($doc) ? file_get_contents($doc) : '') . '</html>';
			return;
		}
		
		header('Content-Type: application/json');
		if (isset($_POST['action']) && $_POST['action'] == 'search') {
			$query = strtoupper(
				str_replace(
					'"', '\\"', preg_replace(
						' {2,}', ' ', preg_replace(
							'(AND|-)', ' ', $_POST['q']
						)
					)
				)
			);
			echo shell_exec('python searchEngine.py -j "'.$query.'"');
			return;
		}
		echo '{}';
	}
?>
