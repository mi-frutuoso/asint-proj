cd microservices/rooms
python3 rooms.py &
cd ../canteen
python3 canteen.py &
cd ../secretariats
python3 secretariats.py &
cd ../../API
python3 API.py &
cd ../server
python3 app.py &
cd ../mobile
python3 mobile.py &
