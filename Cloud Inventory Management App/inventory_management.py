"""
 * Personal License
 *
 * Author: Sujal More
 * Project: Cloud Inventory Management App
 *
 * This code is provided solely for educational and
 * personal use. Unauthorized copying, distribution,
 * or commercial use of this code, in whole or in
 * part, without the explicit permission of the author
 * is strictly prohibited.
 *
 * For permissions or inquiries, please contact:
 * sujalm7200@gmail.com
 *
 * © 2025 Sujal More. All rights reserved.
"""




import streamlit as st
from pymongo import MongoClient

# === Must be first Streamlit command ===
st.set_page_config(page_title="ESA Inventory Tracker", page_icon="📦")

# === MongoDB Setup ===
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client["ESA"]
collection = db["inventory"]


# === Custom ID Utility ===
def create_custom_id(name, location):
    return f"{name.strip().lower().replace(' ', '-')}-{location}"


# === App UI ===
st.title("📦 ESA Inventory Tracker")

menu = st.sidebar.selectbox("Menu", ["View Inventory", "Add Item", "Update Item"])

# === View Inventory ===
if menu == "View Inventory":
    st.header("📋 Current Inventory")
    locations = {"XX323": [], "XX324": [], "XX325": []}

    for item in collection.find():
        loc = item.get("location")
        if loc in locations:
            locations[loc].append(item)

    for loc, items in locations.items():
        st.subheader(f"Location {loc}")
        if items:
            for item in items:
                st.write(f"🆔 `{item['_id']}` — {item['name']} (Qty: {item['quantity']})")
        else:
            st.write("No items.")

# === Add Item ===
elif menu == "Add Item":
    st.header("➕ Add New Item")

    name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    location = st.selectbox("Location", ["XX323", "XX324", "XX325"])

    if st.button("Add Item"):
        item_id = create_custom_id(name, location)

        if collection.find_one({"_id": item_id}):
            st.error("❌ Item already exists at that location. Try updating it instead.")
        else:
            item = {
                "_id": item_id,
                "name": name,
                "quantity": quantity,
                "location": location
            }
            collection.insert_one(item)
            st.success(f"✅ Added `{name}` with ID `{item_id}`")

elif menu == "Update Item":
    st.header("✏️ Update Existing Item")

    # Step 1: Input the ID and load the item
    item_id = st.text_input("Enter Item ID (e.g., `hammer-2`)")

    if "loaded_item" not in st.session_state:
        st.session_state.loaded_item = None

    if st.button("Load Item"):
        item = collection.find_one({"_id": item_id})
        if not item:
            st.error("❌ Item not found.")
            st.session_state.loaded_item = None
        else:
            st.session_state.loaded_item = item

    # Step 2: If item loaded, show the form
    if st.session_state.loaded_item:
        item = st.session_state.loaded_item

        with st.form("update_form"):
            new_name = st.text_input("New Name", value=item["name"])
            new_qty = st.number_input("New Quantity", min_value=0, value=item["quantity"], step=1)
            locations = ["XX323", "XX324", "XX325"]
            new_loc = st.selectbox("New Location", locations, index=locations.index(item["location"]))
            submitted = st.form_submit_button("Update Item")

            if submitted:
                new_id = create_custom_id(new_name, new_loc)
                updated_data = {
                    "name": new_name,
                    "quantity": new_qty,
                    "location": new_loc
                }

                if new_id != item["_id"]:
                    if collection.find_one({"_id": new_id}):
                        st.error("❌ Another item already exists with the new ID.")
                    else:
                        collection.insert_one({**updated_data, "_id": new_id})
                        collection.delete_one({"_id": item["_id"]})
                        st.success(f"✅ Item updated and ID changed to `{new_id}`")
                        st.session_state.loaded_item = None
                        st.rerun()
                else:
                    if (
                            new_name != item["name"]
                            or new_qty != item["quantity"]
                            or new_loc != item["location"]
                    ):
                        collection.update_one({"_id": item["_id"]}, {"$set": updated_data})
                        st.success("✅ Item updated.")
                        st.session_state.loaded_item = None
                        st.rerun()
                    else:
                        st.info("ℹ️ No changes made.")
