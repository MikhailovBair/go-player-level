pipeline {
	agent any
	stages {
		stage('Checkout needed branch') {
			steps {
				sh 'git checkout GOPL-119'
			}
		}
		stage('Install virtualenv') {
			options {
				timeout(time: 1, unit: 'HOURS')
			}
			steps {
				sh 'python3 -m virtualenv venv -p python3'
				sh '. venv/bin/activate'
				sh 'echo . venv/bin/activate > activate_cmd'
				sh 'cat activate_cmd'
			}
		}
		stage('Install Requirements') {
			steps {
				sh '`cat activate_cmd` && python3 -m pip install -r code/get_blunders/requirements.txt'
			}
		}
	}
}