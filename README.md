Electricity portal
PDS project

For all types of data handling, direct SQL queries have been used within the routes.
example:

cur.execute(
            "INSERT INTO Event_Data (device_id, timestamp, label_id, value) VALUES (?, ?, ?, ?)",
            (device_id, form.timestamp.data, form.label_id.data, form.value.data)
        )
        con.commit()
        con.close()