from models import RoomCategory,Room
from database import db
from app import app
# Sample categories



with app.app_context():
    category1= RoomCategory(
        name="Classic",
        pricePerNight= 1200.0,
        image_urls=['https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-227698-208ceffa5daa11ebaeb70242ac110002.jpg?downsize=*:500&crop=990:500',
                    'https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-3867898-00fd0680656511eb81d90242ac110003.jpg?downsize=377:200&crop=377:200',
                    'https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-227698-20c8d3bc5daa11eb8f350242ac110002.jpg?downsize=377:200&crop=377:200'],
        description=["100sq feet","1 Double Bed","1 Bathroom"],
        amenities=["Smoking Room","24-hour HouseKeeping","In-room Dining","Laundary Service"]
    )
    category2 = RoomCategory(
        name="Deluxe",
        pricePerNight=1700.0,
        image_urls=["https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-171430-4bf3e7205daa11eb8d130242ac110002.jpg?downsize=*:500&crop=990:500",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-171430-4b70f81a5daa11eb998a0242ac110002.jpg?downsize=*:500&crop=990:500",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-171430-e930d07638b511ebac140242ac110002.jpg?downsize=*:500&crop=990:500",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-171430-af3303624e8b11ebb22f0242ac110002.jpg?downsize=*:500&crop=990:500"],
        description=["144sq fet","1 Double Bed","1 Bathroom"],
        amenities=["Air Conditioning",
    "Wi-Fi ",
    "Smoking Room", 
    "Bathroom "
    "24-hour Housekeeping "]
    )

    category3 = RoomCategory(
        name="Executive",
        pricePerNight=2200.0,
        image_urls=["https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-1518-a02a55725daa11eb96670242ac110002.jpg?downsize=377:200&crop=377:200",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-1518-9fa4dd205daa11eb908d0242ac110002.jpg?downsize=*:500&crop=990:500",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-1518-a01d48965daa11ebb1680242ac110002.jpg?downsize=*:500&crop=990:500"],
        description=["196sq feet","1 Double Bed","1 Bathroom"],
        amenities=["WiFi", "TV", "Jacuzzi", "Living Room"]
    )

    category4 = RoomCategory(
        name="Suite",
        pricePerNight=2700.0,
        image_urls=["https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-2119-00b376a25dac11eb87e50242ac110002.jpg?downsize=377:200&crop=377:200",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-2119-025552be5dac11eb851d0242ac110002.jpg?downsize=377:200&crop=377:200",
                    "https://r2imghtlak.mmtcdn.com/r2-mmt-htl-image/room-imgs/202011221707135736-2119-01f7434a5dac11eb80200242ac110002.jpg?downsize=377:200&crop=377:200"],
        description=["200sq feet","1 Double Bed","1 Bathroom","City View"],
        amenities=["WiFi", "TV", "Jacuzzi", "Living Room"]
    )

    # Add and commit to DB
    db.session.add_all([category1, category2,category3,category4])
    db.session.commit()

    room1 = Room(
        number="101",
        category_name="Classic",
       
        unavailable_dates=[
            {"from": "2025-08-30", "to": "2025-09-02"}
        ]
    )

    room2 = Room(
        number="102",
        category_name="Deluxe",
        
        unavailable_dates=[
            {"from":"2025-09-02","to":"2025-09-07"},
            {"from":"2025-08-30","to":"2025-09-01"}
        ]
    )

    room3 = Room(
        number="103",
        category_name="Executive",
        
        unavailable_dates=[
        ]
    )

    room4=Room(
        number="104",
        category_name="Suite",
        
        unavailable_dates=[
            {"from":"2025-09-08","to":"2025-09-10"}
        ]
    )

    room5 = Room(
        number="201",
        category_name="Classic",
        
        unavailable_dates=[
            
        ]
    )

    room6=Room(
        number="202",
        category_name="Deluxe",
        
        unavailable_dates=[
            {"from":"2025-09-08","to":"2025-09-10"}
        ]
    )

    db.session.add_all([room1, room2,room3,room4,room5,room6])
    db.session.commit()
