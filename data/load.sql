\COPY company FROM '/home/hk3427/dbms_proj/data/company.csv' DELIMITER ',' CSV HEADER;
\COPY Electric_Vehicle FROM '/home/hk3427/dbms_proj/data/electric_vehicle.csv' DELIMITER ',' CSV HEADER;
\COPY Vehicle_Item FROM '/home/hk3427/dbms_proj/data/vehicle_item.csv' DELIMITER ',' CSV HEADER;
\COPY Vendor FROM '/home/hk3427/dbms_proj/data/vendor.csv' DELIMITER ',' CSV HEADER;
\COPY Vendor_Transactions FROM '/home/hk3427/dbms_proj/data/Vendor_Transactions.csv' DELIMITER ',' CSV HEADER;
\COPY Customer FROM '/home/hk3427/dbms_proj/data/customer.csv' DELIMITER ',' CSV HEADER;
\COPY Customer_Sales FROM '/home/hk3427/dbms_proj/data/customer_sales.csv' DELIMITER ',' CSV HEADER;
\COPY Charging_Stations FROM '/home/hk3427/dbms_proj/data/Charging_Stations.csv' DELIMITER ',' CSV HEADER;
\COPY Charging_Stations_Booking FROM '/home/hk3427/dbms_proj/data/Charging_Stations_Booking.csv' DELIMITER ',' CSV HEADER;
\COPY Service_Reservation FROM '/home/hk3427/dbms_proj/data/Service_Reservation.csv' DELIMITER ',' CSV HEADER;