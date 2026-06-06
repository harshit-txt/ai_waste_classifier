BIN_RULES = {
    "dry_waste" : {
        "bin" : "Blue bin 🔵",
        "color" : "blue",
        "tip" : "Clean before disposing. Recyclable waste",
        "law" : "SWM Rules 2016 — Schedule I"
    },

    "wet_waste" : {
        "bin" : "Green bin 🟢⚫",
        "color" : "green",
        "tip" : "Compostable , Keep seprate for composting",
        "law" : "SWM Rules 2016 — Schedule I"
    },

    "sanitary_waste" : {
        "bin" : "Black waste ⚫",
        "color" : "black",
        "tip" : "wrap before disposing , do not mix with any other waste",
        "law" : "SWM Rules 2016 — Schedule I"
    },

    "e_waste" : {
        "bin" : "⚠ Do not put in any Bin",
        "color" : "red",
        "tip" : "Send to nearest e-collection centre",
        "law" : "E-waste management rules 2022"
    },
}

def get_bin_rule(waste_class):
    if waste_class in BIN_RULES:
        return BIN_RULES[waste_class]
    else:
        return {"bin" : "Unknown" , "tip" : "please scan again"}

        