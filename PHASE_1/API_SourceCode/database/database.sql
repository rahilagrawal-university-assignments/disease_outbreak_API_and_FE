
CREATE TABLE Location (
    country     text PRIMARY KEY 
);

CREATE TABLE Disease (
    name        text PRIMARY KEY,
    symptoms    text
);

CREATE TABLE Outbreak (
    id          char(16) PRIMARY KEY, -- CHECK (id='[0-9]{8}\.[0-9]{7}') PRIMARY KEY , --Wont work for some reason
    date        Date,
    subject     text,
    disease     text,
    FOREIGN KEY (disease) REFERENCES Disease(name)
);

CREATE TABLE outbreakLocation (
    outbreak    text, 
    country     text,
    PRIMARY KEY (outbreak,country),
    FOREIGN KEY (outbreak) REFERENCES Outbreak(id),
    FOREIGN KEY (country) REFERENCES Location(country)
);

INSERT into Disease Values ('Erky', 'Slight Cough or Death');
INSERT into Outbreak Values ('00000000.0000001', '2000-01-01','Test','Erky'); 
INSERT into OutbreakLocation Values ('00000000.0000001','Australia');
INSERT into Disease Values ('aditya', 'Death');
INSERT into Outbreak Values ('00000000.0000002', '2000-01-02','Test','aditya'); 
INSERT into OutbreakLocation Values ('00000000.0000002','Australia');
-- SELECT l.id FROM Location l where (l.Location='Australia');
INSERT into Location VALUES ('Afghanistan');
INSERT into Location VALUES ('Albania');
INSERT into Location VALUES ('Algeria');
INSERT into Location VALUES ('Andorra');
INSERT into Location VALUES ('Angola');
INSERT into Location VALUES ('Anguilla');
INSERT into Location VALUES ('Antigua & Barbuda');
INSERT into Location VALUES ('Argentina');
INSERT into Location VALUES ('Armenia');
INSERT into Location VALUES ('Australia');
INSERT into Location VALUES ('Austria');
INSERT into Location VALUES ('Azerbaijan');
INSERT into Location VALUES ('Bahamas');
INSERT into Location VALUES ('Bahrain');
INSERT into Location VALUES ('Bangladesh');
INSERT into Location VALUES ('Barbados');
INSERT into Location VALUES ('Belarus');
INSERT into Location VALUES ('Belgium');
INSERT into Location VALUES ('Belize');
INSERT into Location VALUES ('Benin');
INSERT into Location VALUES ('Bermuda');
INSERT into Location VALUES ('Bhutan');
INSERT into Location VALUES ('Bolivia');
INSERT into Location VALUES ('Bosnia & Herzegovina');
INSERT into Location VALUES ('Botswana');
INSERT into Location VALUES ('Brazil');
INSERT into Location VALUES ('Brunei Darussalam');
INSERT into Location VALUES ('Bulgaria');
INSERT into Location VALUES ('Burkina Faso');
INSERT into Location VALUES ('Burundi');
INSERT into Location VALUES ('Cambodia');
INSERT into Location VALUES ('Cameroon');
INSERT into Location VALUES ('Canada');
INSERT into Location VALUES ('Cape Verde');
INSERT into Location VALUES ('Cayman Islands');
INSERT into Location VALUES ('Central African Republic');
INSERT into Location VALUES ('Chad');
INSERT into Location VALUES ('Chile');
INSERT into Location VALUES ('China');
INSERT into Location VALUES ('Colombia');
INSERT into Location VALUES ('Comoros');
INSERT into Location VALUES ('Congo');
INSERT into Location VALUES ('Costa Rica');
INSERT into Location VALUES ('Croatia');
INSERT into Location VALUES ('Cuba');
INSERT into Location VALUES ('Cyprus');
INSERT into Location VALUES ('Czech Republic');
INSERT into Location VALUES ('Denmark');
INSERT into Location VALUES ('Djibouti');
INSERT into Location VALUES ('Dominica');
INSERT into Location VALUES ('Dominican Republic');
INSERT into Location VALUES ('Ecuador');
INSERT into Location VALUES ('Egypt');
INSERT into Location VALUES ('El Salvador');
INSERT into Location VALUES ('Equatorial Guinea');
INSERT into Location VALUES ('Eritrea');
INSERT into Location VALUES ('Estonia');
INSERT into Location VALUES ('Ethiopia');
INSERT into Location VALUES ('Fiji');
INSERT into Location VALUES ('Finland');
INSERT into Location VALUES ('France');
INSERT into Location VALUES ('French Guiana');
INSERT into Location VALUES ('Gabon');
INSERT into Location VALUES ('Gambia');
INSERT into Location VALUES ('Georgia');
INSERT into Location VALUES ('Germany');
INSERT into Location VALUES ('Ghana');
INSERT into Location VALUES ('Great Britain');
INSERT into Location VALUES ('Greece');
INSERT into Location VALUES ('Grenada');
INSERT into Location VALUES ('Guadeloupe');
INSERT into Location VALUES ('Guatemala');
INSERT into Location VALUES ('Guinea');
INSERT into Location VALUES ('Guinea-Bissau');
INSERT into Location VALUES ('Guyana');
INSERT into Location VALUES ('Haiti');
INSERT into Location VALUES ('Honduras');
INSERT into Location VALUES ('Hungary');
INSERT into Location VALUES ('Iceland');
INSERT into Location VALUES ('India');
INSERT into Location VALUES ('Indonesia');
INSERT into Location VALUES ('Iran');
INSERT into Location VALUES ('Iraq');
INSERT into Location VALUES ('Israel');
INSERT into Location VALUES ('Italy');
INSERT into Location VALUES ('Ivory Coast');
INSERT into Location VALUES ('Jamaica');
INSERT into Location VALUES ('Japan');
INSERT into Location VALUES ('Jordan');
INSERT into Location VALUES ('Kazakhstan');
INSERT into Location VALUES ('Kenya');
INSERT into Location VALUES ('North Korea');
INSERT into Location VALUES ('South Korea');
INSERT into Location VALUES ('Kosovo');
INSERT into Location VALUES ('Kuwait');
INSERT into Location VALUES ('Kyrgyzstan');
INSERT into Location VALUES ('Laos');
INSERT into Location VALUES ('Latvia');
INSERT into Location VALUES ('Lebanon');
INSERT into Location VALUES ('Lesotho');
INSERT into Location VALUES ('Liberia');
INSERT into Location VALUES ('Libya');
INSERT into Location VALUES ('Liechtenstein');
INSERT into Location VALUES ('Lithuania');
INSERT into Location VALUES ('Luxembourg');
INSERT into Location VALUES ('Madagascar');
INSERT into Location VALUES ('Malawi');
INSERT into Location VALUES ('Malaysia');
INSERT into Location VALUES ('Maldives');
INSERT into Location VALUES ('Mali');
INSERT into Location VALUES ('Malta');
INSERT into Location VALUES ('Martinique');
INSERT into Location VALUES ('Mauritania');
INSERT into Location VALUES ('Mauritius');
INSERT into Location VALUES ('Mayotte');
INSERT into Location VALUES ('Mexico');
INSERT into Location VALUES ('Moldova');
INSERT into Location VALUES ('Monaco');
INSERT into Location VALUES ('Mongolia');
INSERT into Location VALUES ('Montenegro');
INSERT into Location VALUES ('Montserrat');
INSERT into Location VALUES ('Morocco');
INSERT into Location VALUES ('Mozambique');
INSERT into Location VALUES ('Myanmar/Burma');
INSERT into Location VALUES ('Namibia');
INSERT into Location VALUES ('Nepal');
INSERT into Location VALUES ('New Zealand');
INSERT into Location VALUES ('Nicaragua');
INSERT into Location VALUES ('Niger');
INSERT into Location VALUES ('Nigeria');
INSERT into Location VALUES ('North Macedonia');
INSERT into Location VALUES ('Norway');
INSERT into Location VALUES ('Oman');
INSERT into Location VALUES ('Pacific Islands');
INSERT into Location VALUES ('Pakistan');
INSERT into Location VALUES ('Panama');
INSERT into Location VALUES ('Papua New Guinea');
INSERT into Location VALUES ('Paraguay');
INSERT into Location VALUES ('Peru');
INSERT into Location VALUES ('Philippines');
INSERT into Location VALUES ('Poland');
INSERT into Location VALUES ('Portugal');
INSERT into Location VALUES ('Puerto Rico');
INSERT into Location VALUES ('Qatar');
INSERT into Location VALUES ('Reunion');
INSERT into Location VALUES ('Romania');
INSERT into Location VALUES ('Russian Federation');
INSERT into Location VALUES ('Rwanda');
INSERT into Location VALUES ('Saint Kitts and Nevis');
INSERT into Location VALUES ('Saint Lucia');
INSERT into Location VALUES ('Saint Vincent and the Grenadines');
INSERT into Location VALUES ('Samoa');
INSERT into Location VALUES ('Sao Tome and Principe');
INSERT into Location VALUES ('Saudi Arabia');
INSERT into Location VALUES ('Senegal');
INSERT into Location VALUES ('Serbia');
INSERT into Location VALUES ('Seychelles');
INSERT into Location VALUES ('Sierra Leone');
INSERT into Location VALUES ('Singapore');
INSERT into Location VALUES ('Slovakia');
INSERT into Location VALUES ('Slovenia');
INSERT into Location VALUES ('Solomon Islands');
INSERT into Location VALUES ('Somalia');
INSERT into Location VALUES ('South Africa');
INSERT into Location VALUES ('South Sudan');
INSERT into Location VALUES ('Spain');
INSERT into Location VALUES ('Sri Lanka');
INSERT into Location VALUES ('Sudan');
INSERT into Location VALUES ('Suriname');
INSERT into Location VALUES ('Swaziland');
INSERT into Location VALUES ('Sweden');
INSERT into Location VALUES ('Switzerland');
INSERT into Location VALUES ('Syria');
INSERT into Location VALUES ('Tajikistan');
INSERT into Location VALUES ('Tanzania');
INSERT into Location VALUES ('Thailand');
INSERT into Location VALUES ('Netherlands');
INSERT into Location VALUES ('Timor Leste');
INSERT into Location VALUES ('Togo');
INSERT into Location VALUES ('Trinidad & Tobago');
INSERT into Location VALUES ('Tunisia');
INSERT into Location VALUES ('Turkey');
INSERT into Location VALUES ('Turkmenistan');
INSERT into Location VALUES ('Turks & Caicos Islands');
INSERT into Location VALUES ('Uganda');
INSERT into Location VALUES ('Ukraine');
INSERT into Location VALUES ('United Arab Emirates');
INSERT into Location VALUES ('USA');
INSERT into Location VALUES ('Uruguay');
INSERT into Location VALUES ('Uzbekistan');
INSERT into Location VALUES ('Venezuela');
INSERT into Location VALUES ('Vietnam');
INSERT into Location VALUES ('Virgin Islands');
INSERT into Location VALUES ('Yemen');
INSERT into Location VALUES ('Zambia');
INSERT into Location VALUES ('Zimbabwe');
