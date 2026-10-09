from src import database
from src.models import Status


def get_applications():
    con = database.get_connection()
    rows = con.execute(
        "SELECT id, company, role, status, applied_date, notes FROM applications"
    ).fetchall()
    con.close()
    result = []
    for row in rows:
        result.append(
            {
                "id": row["id"],
                "company": row["company"],
                "role": row["role"],
                "status": row["status"],
                "applied_date": row["applied_date"],
                "notes": row["notes"],
            }
        )
    return result


def get_application(application_id):
    con = database.get_connection()
    row = con.execute(
        "SELECT id, company, role, status, applied_date, notes FROM applications WHERE id = ?",
        (application_id,),
    ).fetchone()
    con.close()
    if row is None:
        raise ValueError("App not found")
    return {
        "id": row["id"],
        "company": row["company"],
        "role": row["role"],
        "status": row["status"],
        "applied_date": row["applied_date"],
        "notes": row["notes"],
    }


def add_application(company, role, status, applied_date, notes=None):
    con = database.get_connection()
    status_value = Status(status).value
    cur = con.execute(
        "INSERT INTO applications (company, role, status, applied_date, notes) VALUES (?,?,?,?,?)",
        (
            company,
            role,
            status_value,
            applied_date,
            notes,
        ),
    )
    con.commit()
    new_id = cur.lastrowid
    con.close()
    return {
        "id": new_id,
        "company": company,
        "role": role,
        "status": status_value,
        "applied_date": applied_date,
        "notes": notes,
    }


def update_status_application(application_id, status):
    con = database.get_connection()
    status_value = Status(status).value
    cur = con.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (
            status_value,
            application_id,
        ),
    )
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise ValueError("App not found")
    return get_application(application_id)


def delete_application(application_id):
    con = database.get_connection()
    cur = con.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise ValueError("App not found")
