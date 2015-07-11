chainerapp
=====================
## Requiements

- Docker (>=1.6)
- mac os?

## How to use

####Fork & Clone
- https://github.com/(GIT_ID)/chainer.git
- https://github.com/(GIT_ID)//chainerapp.git


####First Setting
ex.
vi ~/.bash_profile
exportGIT_HOME=/Users/(OS_ID)/git

####Build DockerImage
  $ ./1_build_chainerapp-test.sh

####Start Container
  $ ./2_run_chainerapp-test.sh

####Stop & Delete Container
  $ ./3_stop_chainerapp-test.sh

####Login Container
  $ ./4_exec_chainerapp-test.sh
