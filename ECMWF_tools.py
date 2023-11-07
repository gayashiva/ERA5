import os
import cdsapi
import ECMWF_query

class ECMWF_tools:
    def __init__(self, **kwargs):
        for key in kwargs:
            # print(f"%s -> %s" % (key, kwargs[key]))
            self.config_ecmwf = ECMWF_query.ECMWF_query(**kwargs)
            # setattr(self, key, kwargs[key])
        # https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means?tab=form
        # https://confluence.ecmwf.int/pages/viewpage.action?pageId=82870405#ERA5:datadocumentation-Table4
        # Check data availability: http://apps.ecmwf.int/datasets/

        self.server = cdsapi.Client(debug=self.config_ecmwf.debug)

    def create_requests(self):
        years = [
            y
            for y in range(self.config_ecmwf.start_year, self.config_ecmwf.end_year + 1)
        ]
        print(years)

        if not os.path.exists(self.config_ecmwf.resultsdir):
            os.mkdir(self.config_ecmwf.resultsdir)
        for year in years:

            print("=> Downloading for year {}".format(year))

            for parameter in self.config_ecmwf.parameters:
                print("=> getting data for : {} ".format(parameter))

                metadata = self.config_ecmwf.get_parameter_metadata(parameter)

                # out_filename = "{}{}_{}_year_{}_{}.grib".format(
                out_filename = "{}{}_{}_year_{}_{}.nc".format(
                    self.config_ecmwf.resultsdir,
                    self.config_ecmwf.dataset,
                    metadata["short_name"],
                    year,
                    self.config_ecmwf.reanalysis,
                )

                if os.path.exists(out_filename):
                    if self.overwrite:
                        print("Overwriting File")
                        os.remove(out_filename)
                        self.submit_request(parameter, year, out_filename)
                    else:
                        print("File exists")
                else:
                    self.submit_request(parameter, year, out_filename)

    def submit_request(self, parameter, year, out_filename):

        options = {
            "product_type": "reanalysis",
            "year": year,
            "month": [
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
            ],
            "day": [
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
            ],
            "time": [
                "00:00",
                "01:00",
                "02:00",
                "03:00",
                "04:00",
                "05:00",
                "06:00",
                "07:00",
                "08:00",
                "09:00",
                "10:00",
                "11:00",
                "12:00",
                "13:00",
                "14:00",
                "15:00",
                "16:00",
                "17:00",
                "18:00",
                "19:00",
                "20:00",
                "21:00",
                "22:00",
                "23:00",
            ],
            "variable": [parameter],
            # "format": "grib",
            "format": "netcdf",
            "area": self.config_ecmwf.area,
            # "area": area,
            # "verbose": self.config_ecmwf.debug,
        }
        # # Add more specific options for variables on pressure surfaces
        # if parameter == "specific_humidity":
        # self.config_ecmwf.reanalysis = "reanalysis-era5-pressure-levels"
        # options["levtype"] = "pl"
        # options["pressure_level"] = "1000"
        # else:
        # self.config_ecmwf.reanalysis = "reanalysis-era5-single-levels"

        try:
            # Do the request
            self.server.retrieve(self.config_ecmwf.reanalysis, options, out_filename)
        except Exception as e:
            print(e)
            print(
                "[!] -------------------------- PROBLEMS WITH {0}".format(out_filename)
            )

        # metadata = self.config_ecmwf.get_parameter_metadata(parameter)

        # converter = ECMWF_convert_to_ROMS.ECMWF_convert_to_ROMS()
        # converter.convert_to_ROMS_standards(
        # out_filename, metadata, parameter, self.config_ecmwf
        # )


if __name__ == "__main__":
    # locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
    # locations = ["schwarzsee", "diavolezza"]
    # locations = ["guttannen", "leh"]
    # locations = ["central_asia2"]
    locations = ["south_america", "europe", "north_america", "central_asia", "leh"]
    for key in locations:
        print(f"\n\tLocation -> %s" % (key))
        tool = ECMWF_tools(location=key)
        tool.create_requests()
