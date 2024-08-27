import ast
import datetime
from helper import *
from dictionaries import *


class VINDecoder:
    def __init__(self, patterns_df):
        self.vin = None
        self.make_model = None
        self.patterns_df = patterns_df
        self.ar_names_analyzer = None
        self.include_market_value = True

    def model_pattern(self, VIN, wmi):
        final_df = self.patterns_df
        f_df = final_df[final_df['wmi'] == wmi]
        if f_df.empty:
            return wmi, 'unknown'
        make = f_df.iloc[0]['make']
        matched_list = []
        if f_df.empty:
            return None
        model_code = VIN[3:8]
        for index, row in f_df.iterrows():
            patterns = ast.literal_eval(row['pattern'])
            for p in patterns:
                if re.search(p, model_code):
                    matched_list.append({p: row['model']})
        return make, refine_car_model_name(find_longest_match(matched_list, model_code))

    @property
    def is_valid(self):
        """
        Returns True if a VIN is valid, otherwise returns False.
        """
        if len(self.vin) != 17:
            return False

        prohibited_chars = 'IOQ'
        if any(char in prohibited_chars for char in self.vin):
            return False

        # invalid_tenth_char = 'UZ0'
        # if self.vin[9] in invalid_tenth_char:
        #     logger.logging.error(f"Invalid tenth character in VIN: {self.vin[9]}")
        #     return False

        return True

    @property
    def is_wmi_exist(self):
        wmi = self.wmi
        return wmi[:3] in list(WMI_MAP.keys())
    @property
    def region(self):
        """
        Returns the World Manufacturer's Region.
        """
        first_char = self.vin[0]
        return WORLD_MANUFACTURER_MAP.get(first_char, {}).get('region', 'Unknown')


    @property
    def vsn(self):
        """
        Returns the Vehicle Sequential Number.
        """
        return self.vin[-6:]

    @property
    def wmi(self):
        """
        Returns the World Manufacturer Identifier (any standards).
        """
        return self.vin[0:3]

    @property
    def make(self):
        """
        Returns the World Manufacturer Make name.
        """
        en_make_name = self.make_model[0]
        ar_make_name = get_ar_make_name(self.ar_names_analyzer, en_make_name)
        return {"ar_name": ar_make_name, "en_name": en_make_name}

    @property
    def manufacturer(self):
        wmi = self.wmi
        if (wmi[:3] in WMI_MAP):
            return WMI_MAP[wmi[:3]]
        return WMI_MAP.get(wmi, 'Unknown')

    @property
    def year(self):
        """
        Returns the model year of the vehicle.
        """
        try:
            if (YEARS_CODES_PRE_2040.get(self.vin[9]) <= datetime.date.today().year):
                year = max(YEARS_CODES_PRE_2040.get(self.vin[9]), YEARS_CODES_PRE_2010.get(self.vin[9]))
            else:
                year = YEARS_CODES_PRE_2010.get(self.vin[9])
            return year
        except Exception:
            return 0
    @property
    def model(self):
        """
        Returns the car model name.
        """
        en_model_name = self.make_model[1]
        ar_model_name = get_ar_model_name(self.ar_names_analyzer, en_model_name)
        return {"ar_name": ar_model_name, "en_name": en_model_name}

    def make_model_extractor(self):
        makes_list = list(WMI_MAP.keys())
        if self.vin[0:3] in makes_list:
            self.make_model = self.model_pattern(self.vin, self.vin[0:3])
        else:
            self.make_model = 'Unknown', 'Unknown'
        return self.make_model

    def decode(self):
        make_model = self.make_model_extractor()
        if make_model is not None:
            result = {
                "VIN": self.vin,
                "Make": make_model[0],
                "Model": make_model[1],
                "Year": self.year,
                "Manufacturer": self.manufacturer.strip("\""),
                "Region": self.region.capitalize(),
                "WMI": self.wmi,
                "Serial": self.vsn,
            }
            return result
        return {}