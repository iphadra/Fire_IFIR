from Fire_detection_algorithm import *
parameters = {
    "day initial": "2020-06-03",
    "day final": "2020-09-28",
    "city": "Parana",
    "fig x": 360.5,
    "fig y": 358.5,
    "lon": [-61, -60],
    "lat": [-33.5, -32.5],
    "delta": 0.25,
    "path data": "../Data_FIRMS/suomi/South_America/",
    "path graphics": "../Graphics/",
    "path results": "../Archivos/",
}
Fire = Fire(parameters["path data"],
            parameters["city"],
            parameters["day initial"],
            parameters["day final"],
            parameters["fig x"],
            parameters["fig y"],
            parameters["lon"],
            parameters["lat"],
            parameters["delta"])
Fire.read_filenames()
Fire.read_map(parameters["path graphics"], "map2.png")
Fire.algorithm(parameters["path results"],
               parameters["path graphics"])
Fire.create_animation()
