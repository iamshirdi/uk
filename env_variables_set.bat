cd ./
set FLASK_APP=app.py
set FLASK_DEBUG=1
set DATABASE_URL=postgres://jcmvfiwafkhuxg:343667b95bfa637b59dabf4be288f1ee6da256a59ee3680ff34163d6e57bc545@ec2-46-137-91-216.eu-west-1.compute.amazonaws.com:5432/d5uqu65fvr5lo3
echo %DATABASE_URL%
cmd /k
::FLASK_DEBUG to 1, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.
