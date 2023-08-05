import sqlite3

class TableHandler:

    def make_blueprint(self, data: list, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Reminds (user_id, user_timezone, remind_name, remind_timedata, blueprint) VALUES(?, ?, ?, ?, ?)",
            (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
            )
        )

        conn.commit()

    def get_blueprints(self, data, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Reminds WHERE user_id = ? AND blueprint = 1", (data,)
        )

        result = cur.fetchall()
        conn.commit()

        return result



    def create_remind(self, data: list, conn:sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Reminds WHERE user_id = ? AND user_timezone = ? AND blueprint = 1", (data[0], data[1],)
        )

        result = cur.fetchone()

        cur.execute(
            "INSERT INTO Reminds (user_id, user_timezone, remind_name, remind_timedata, blueprint) VALUES(?, ?, ?, ?, ?)",(
                result[1], result[2], result[3], result[4], 0
            )
        )

        conn.commit()


    # def get_by_user(self, data: int, conn: sqlite3.Connection):
    #     cur = conn.cursor()
    #     cur.execute(
    #         "SELECT * FROM Reminds WHERE user_id = ? ORDER BY id DESC", (data,)
    #     )
    #
    #     result = cur.fetchone()
    #     conn.commit()
    #
    #     return result

    def set_name_time(self, data: list, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "UPDATE Reminds SET remind_name = ?, remind_timedata = ? WHERE user_id = ? AND user_timezone = ? AND blueprint = 0",
            (
                data[2], data[3], data[0], data[1],
            )
        )

        conn.commit()

    def get_by_datetime(self, data: list, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Reminds WHERE user_id = ? AND user_timezone = ? AND remind_timedata = ? AND blueprint = 0", (data[0], data[1], data[2],)
        )

        result = cur.fetchone()
        conn.commit()

        return result

    def delete(self, data: list, conn: sqlite3.Connection):
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM Reminds WHERE user_id = ? AND remind_timedata = ? AND remind_name = ? AND user_timezone = ? "
            "AND blueprint = 0",
            (data[0], data[1], data[2], data[3],)
        )

        conn.commit()


# доделать еще чтоб смотрело на таймзон когда удаляет


