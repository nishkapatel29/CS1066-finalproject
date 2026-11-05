import datetime as dt

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Daytrip Planner",
    page_icon="🗺️",
    layout="wide",
)

st.title("Daytrip Planner")
st.caption("Add destinations, set your daily schedule, and choose how long to spend at each stop.")

with st.sidebar:
    st.header("Trip setup")
    number_of_days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=7,
        value=2,
        step=1,
        key="number_of_days",
    )
    st.info("Set a start and end time and location for each day.")

if "destinations" not in st.session_state:
    st.session_state.destinations = pd.DataFrame(
        [
            {
                "Destination": "Boston Common",
                "Address / area": "139 Tremont St",
                "Opens": dt.time(6, 0),
                "Closes": dt.time(23, 30),
                "Visit (min)": 60,
                "Day": 1,
                "Fixed reservation": False,
                "Reservation time": None,
            },
            {
                "Destination": "Museum of Fine Arts",
                "Address / area": "465 Huntington Ave",
                "Opens": dt.time(10, 0),
                "Closes": dt.time(17, 0),
                "Visit (min)": 120,
                "Day": 1,
                "Fixed reservation": True,
                "Reservation time": dt.time(11, 0),
            },
            {
                "Destination": "Isabella Stewart Gardner Museum",
                "Address / area": "25 Evans Way",
                "Opens": dt.time(11, 0),
                "Closes": dt.time(17, 0),
                "Visit (min)": 90,
                "Day": 2,
                "Fixed reservation": False,
                "Reservation time": None,
            },
        ]
    )

destinations = st.session_state.destinations.copy()
destinations["Day"] = (
    pd.to_numeric(destinations["Day"], errors="coerce")
    .fillna(1)
    .clip(1, number_of_days)
    .astype(int)
)
st.session_state.destinations = destinations

st.header("Daily schedule")
day_tabs = st.tabs([f"Day {day}" for day in range(1, number_of_days + 1)])
day_settings = []

for day_number, tab in enumerate(day_tabs, start=1):
    with tab:
        start_col, end_col = st.columns(2)
        with start_col:
            start_location = st.text_input(
                "Starting location",
                value="Hotel or starting address" if day_number == 1 else "",
                key=f"day_{day_number}_start_location",
                placeholder="Enter an address or place",
            )
            start_time = st.time_input(
                "Day starts",
                value=dt.time(9, 0),
                key=f"day_{day_number}_start_time",
            )
        with end_col:
            end_location = st.text_input(
                "Ending location",
                value="Hotel or ending address" if day_number == 1 else "",
                key=f"day_{day_number}_end_location",
                placeholder="Enter an address or place",
            )
            end_time = st.time_input(
                "Day ends",
                value=dt.time(18, 0),
                key=f"day_{day_number}_end_time",
            )
        day_settings.append(
            {
                "start_location": start_location,
                "start_time": start_time,
                "end_location": end_location,
                "end_time": end_time,
            }
        )

st.header("Destinations")
st.caption(
    "Add or edit stops below. Each destination can be assigned to a day; "
    "a fixed reservation is associated with that day."
)

edited_destinations = st.data_editor(
    st.session_state.destinations,
    key="destination_editor",
    num_rows="dynamic",
    hide_index=True,
    width="stretch",
    column_config={
        "Destination": st.column_config.TextColumn(
            "Destination", required=True, help="Name of the place to visit."
        ),
        "Address / area": st.column_config.TextColumn("Address / area"),
        "Opens": st.column_config.TimeColumn("Opens", format="HH:mm"),
        "Closes": st.column_config.TimeColumn("Closes", format="HH:mm"),
        "Visit (min)": st.column_config.NumberColumn(
            "Visit (min)", min_value=0, max_value=1440, step=15, format="%d"
        ),
        "Day": st.column_config.NumberColumn(
            "Day", min_value=1, max_value=number_of_days, step=1, format="%d"
        ),
        "Fixed reservation": st.column_config.CheckboxColumn(
            "Fixed reservation"
        ),
        "Reservation time": st.column_config.TimeColumn(
            "Reservation time", format="HH:mm"
        ),
    },
)
st.session_state.destinations = edited_destinations

if "trip_generated" not in st.session_state:
    st.session_state.trip_generated = False

if st.button("Generate trip", type="primary"):
    st.session_state.trip_generated = True

if not st.session_state.trip_generated:
    st.info("When your trip details are ready, select **Generate trip** to preview them.")
else:
    st.header("Trip preview")
    st.caption(
        "This preview uses the assigned days and the order destinations were entered. "
        "It does not calculate travel times, check feasibility, or optimize the route."
    )

    if edited_destinations.empty:
        st.info("Add destinations above, then select **Generate trip**.")
    else:
        for day_number, settings in enumerate(day_settings, start=1):
            day_destinations = edited_destinations[
                pd.to_numeric(edited_destinations["Day"], errors="coerce")
                .fillna(0)
                .astype(int)
                == day_number
            ]

            with st.container(border=True):
                st.subheader(f"Day {day_number}")
                start_text = settings["start_time"].strftime("%I:%M %p")
                end_text = settings["end_time"].strftime("%I:%M %p")
                st.write(
                    f"**{start_text}** — Start: "
                    f"{settings['start_location'] or 'Not set'}"
                )

                if day_destinations.empty:
                    st.caption("No destinations assigned to this day yet.")
                else:
                    for _, destination in day_destinations.iterrows():
                        name = str(destination["Destination"]).strip()
                        if not name:
                            name = "Unnamed destination"
                        address = str(destination["Address / area"]).strip()
                        visit_minutes = destination["Visit (min)"]
                        visit_text = (
                            f"{int(visit_minutes)} min"
                            if pd.notna(visit_minutes)
                            else "Visit duration not set"
                        )
                        opening = destination["Opens"]
                        closing = destination["Closes"]
                        hours_text = (
                            f"{opening.strftime('%I:%M %p')}–"
                            f"{closing.strftime('%I:%M %p')}"
                            if isinstance(opening, dt.time)
                            and isinstance(closing, dt.time)
                            else "Opening hours not set"
                        )
                        reservation = ""
                        if destination["Fixed reservation"]:
                            reservation_time = destination["Reservation time"]
                            reservation = (
                                f" · Reservation: {reservation_time.strftime('%I:%M %p')}"
                                if isinstance(reservation_time, dt.time)
                                else " · Reservation time not set"
                            )

                        st.markdown(
                            f"- **{name}** — {visit_text} · "
                            f"Open {hours_text}{reservation}"
                        )
                        if address:
                            st.caption(address)

                st.write(
                    f"**{end_text}** — End: "
                    f"{settings['end_location'] or 'Not set'}"
                )
