import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import streamlit as st
from functions import (
    login, register,
    get_available_books, get_user_orders,
    place_order, remove_order_item,
    get_all_books, add_book, delete_book, get_all_orders,
    get_inventory, add_to_inventory, update_inventory_quantity,
    remove_from_inventory, get_all_shelves
)

st.set_page_config(page_title="BookOps", layout="wide", initial_sidebar_state="collapsed")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --ink:      #1a1a18;
  --ink-2:    #4a4a46;
  --ink-3:    #8a8a84;
  --paper:    #f8f6f1;
  --paper-2:  #efece6;
  --amber:    #c97c2a;
  --amber-lt: #f5e9d4;
  --red:      #b83232;
  --red-lt:   #faeaea;
  --green:    #2e7d46;
  --green-lt: #e6f4eb;
  --border:   rgba(26,26,24,0.12);
  --radius:   10px;
  --shadow:   0 2px 12px rgba(26,26,24,0.08);
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: var(--paper);
  color: var(--ink);
}

/* grid background on the main app area */
.stApp {
  background-color: var(--paper);
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 47px, rgba(26,26,24,0.07) 47px, rgba(26,26,24,0.07) 48px),
    repeating-linear-gradient(90deg, transparent, transparent 47px, rgba(26,26,24,0.07) 47px, rgba(26,26,24,0.07) 48px);
}


/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* headings */
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; font-weight: 400 !important; }

/* buttons */
.stButton > button {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  border-radius: 8px;
  border: 1px solid var(--ink);
  background: var(--ink);
  color: #fff;
  padding: 8px 20px;
  transition: background 0.18s;
}
.stButton > button:hover { background: #2e2e2a; border-color: #2e2e2a; }

/* inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
  font-family: 'DM Sans', sans-serif;
  border-radius: 8px;
  border: 1px solid rgba(26,26,24,0.22);
  background: #fff;
  color: var(--ink);
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
  border-bottom: 1px solid var(--border);
  background: transparent;
  gap: 4px;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-3);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
  color: var(--ink) !important;
  border-bottom: 2px solid var(--amber) !important;
  background: transparent !important;
}

/* card */
.bookops-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 0.75rem;
  transition: box-shadow 0.18s, transform 0.18s;
}
.bookops-card:hover { box-shadow: 0 4px 20px rgba(26,26,24,0.12); transform: translateY(-2px); }

/* badge */
.badge-amber { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; background:var(--amber-lt); color:var(--amber); }
.badge-gray  { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; background:var(--paper-2); color:var(--ink-3); }
.badge-green { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; background:var(--green-lt); color:var(--green); }
.badge-red   { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; background:var(--red-lt); color:var(--red); }

/* stat card */
.stat-card { background:var(--paper-2); border-radius:8px; padding:1rem; text-align:left; }
.stat-val  { font-family:'DM Serif Display',serif; font-size:1.6rem; color:var(--ink); }
.stat-lbl  { font-size:12px; color:var(--ink-3); margin-top:2px; }

/* nav bar */
.bookops-nav {
  background: #fff;
  border-bottom: 1px solid var(--border);
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 58px;
  margin: -2rem -4rem 2rem -4rem;
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-brand { font-family:'DM Serif Display',serif; font-size:1.4rem; color:var(--ink); }
.nav-brand span { color:var(--amber); }
.nav-user  { font-size:13px; color:var(--ink-3); }

/* auth screen grid bg */
.auth-bg {
  background-color: var(--paper);
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 47px, rgba(26,26,24,0.12) 47px, rgba(26,26,24,0.12) 48px),
    repeating-linear-gradient(90deg, transparent, transparent 47px, rgba(26,26,24,0.12) 47px, rgba(26,26,24,0.12) 48px);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* success / error messages */
.stSuccess { border-radius: 8px; }
.stError   { border-radius: 8px; }

/* table styling */
.stDataFrame { border-radius: var(--radius); overflow: hidden; }

/* danger button override via key */
[data-testid="danger-btn"] > button {
  background: var(--red-lt) !important;
  color: var(--red) !important;
  border-color: var(--red) !important;
}
[data-testid="danger-btn"] > button:hover {
  background: var(--red) !important;
  color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "toast" not in st.session_state:
    st.session_state.toast = None  # ("msg", "success"|"error")
if "reg_key" not in st.session_state:
    st.session_state.reg_key = 0
if "admin_tab" not in st.session_state:
    st.session_state.admin_tab = 0

def set_active_tab(index):
    st.session_state.admin_tab = index

def inject_tab_js(index):
    st.markdown(f"""
    <script>
    (function() {{
        function clickTab() {{
            var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
            if (tabs.length > {index}) {{
                tabs[{index}].click();
            }} else {{
                setTimeout(clickTab, 100);
            }}
        }}
        setTimeout(clickTab, 150);
    }})();
    </script>
    """, unsafe_allow_html=True)

def set_toast(msg, kind="success"):
    st.session_state.toast = (msg, kind)

def show_toast():
    if st.session_state.toast:
        msg, kind = st.session_state.toast
        if kind == "success":
            st.success(msg)
        else:
            st.error(msg)
        st.session_state.toast = None

def logout():
    st.session_state.user = None

# ── Navbar ────────────────────────────────────────────────────────────────────
def navbar(username, role):
    admin_badge = ' <span style="font-size:11px;color:var(--amber);font-weight:500;letter-spacing:.05em;">ADMIN</span>' if role == "admin" else ""
    st.markdown(f"""
    <div class="bookops-nav">
      <span class="nav-brand">Book<span>Ops</span>{admin_badge}</span>
      <span class="nav-user">{username}</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AUTH SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def screen_auth():
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;margin-bottom:2rem">
          <h1 style="font-size:2rem">Book<span style="color:var(--amber)">Ops</span></h1>
          <p style="color:var(--ink-3);font-size:14px">Bookstore management system</p>
        </div>
        """, unsafe_allow_html=True)

        show_toast()

        tab_login, tab_register = st.tabs(["Sign in", "Create account"])

        with tab_login:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="e.g. alice_reads", key="login_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            if st.button("Sign in", use_container_width=True, key="btn_login"):
                if not username or not password:
                    set_toast("Enter your username and password.", "error")
                    st.rerun()
                user = login(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    set_toast("Incorrect username or password.", "error")
                    st.rerun()

        with tab_register:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            k = st.session_state.reg_key
            new_user  = st.text_input("Username", placeholder="Choose a username", key=f"reg_user_{k}")
            new_email = st.text_input("Email", placeholder="you@example.com", key=f"reg_email_{k}")
            new_pass  = st.text_input("Password", type="password", placeholder="Min. 6 characters", key=f"reg_pass_{k}")
            if st.button("Create account", use_container_width=True, key="btn_register"):
                if not new_user or not new_email or not new_pass:
                    set_toast("Fill in all fields.", "error")
                    st.rerun()
                elif len(new_pass) < 6:
                    set_toast("Password must be at least 6 characters.", "error")
                    st.rerun()
                else:
                    success, msg = register(new_user, new_pass, new_email)
                    if success:
                        st.session_state.reg_key += 1
                        set_toast("Account created! Sign in to continue.", "success")
                        st.rerun()
                    else:
                        set_toast(msg, "error")
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# USER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def screen_user():
    user = st.session_state.user
    navbar(user["username"], "user")

    st.markdown(f"""
    <div style="margin-bottom:1.5rem">
      <h2>Welcome back, {user['username']}</h2>
      <p style="color:var(--ink-3);font-size:14px">Browse available books or check your orders below.</p>
    </div>
    """, unsafe_allow_html=True)

    show_toast()

    _, col_logout = st.columns([6, 1])
    with col_logout:
        if st.button("Sign out", key="user_logout"):
            logout()
            st.rerun()

    tab_browse, tab_orders = st.tabs(["Browse books", "My orders"])

    # ── Browse tab ────────────────────────────────────────────────────────────
    with tab_browse:
        books = get_available_books()

        fcol1, fcol2 = st.columns([2, 1])
        with fcol1:
            search = st.text_input("", placeholder="Search by title…", key="u_search", label_visibility="collapsed")
        with fcol2:
            categories = ["All categories"] + sorted(set(b["Category"] for b in books))
            cat_filter = st.selectbox("", categories, key="u_cat", label_visibility="collapsed")

        filtered = [
            b for b in books
            if (not search or search.lower() in b["Title"].lower())
            and (cat_filter == "All categories" or b["Category"] == cat_filter)
        ]

        st.markdown(f'<p style="font-size:12px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem">{len(filtered)} book{"s" if len(filtered) != 1 else ""}</p>', unsafe_allow_html=True)

        if not filtered:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:var(--ink-3)">
              <div style="font-size:2.5rem">📚</div>
              <h3>No books found</h3>
              <p style="font-size:14px">Try a different search or category.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            cols = st.columns(3)
            for i, book in enumerate(filtered):
                qty = book["QuantityAvailable"]
                qty_color = "var(--red)" if qty <= 1 else "var(--green)"
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="bookops-card">
                      <span class="badge-amber">{book['Category']}</span>
                      <p style="font-weight:500;font-size:15px;margin:.5rem 0 .25rem">{book['Title']}</p>
                      <p style="font-size:13px;color:var(--ink-2);line-height:1.5;min-height:40px">{book.get('Description') or '—'}</p>
                      <p style="font-size:13px;color:var(--ink-3);margin:.5rem 0">{book['YearPublished']} &nbsp;·&nbsp; {book['Pages']} pages</p>
                      <p style="font-size:12px;background:var(--paper-2);padding:6px 10px;border-radius:6px;color:var(--ink-3)">
                        📍 {book['Hall']}, {book['Building']}, Floor {book['Floor']}
                      </p>
                      <p style="font-size:13px;font-weight:500;color:{qty_color};margin-top:.5rem">{qty} available</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.form(key=f"order_form_{book['book_id']}_{i}"):
                        qty_input = st.number_input("Quantity", min_value=1, max_value=int(qty), value=1, key=f"qty_{book['book_id']}_{i}")
                        submitted = st.form_submit_button("Order", use_container_width=True)
                        if submitted:
                            success, msg = place_order(
                                user["account_id"],
                                book["book_id"],
                                book.get("shelf_id"),
                                int(qty_input)
                            )
                            set_toast(msg, "success" if success else "error")
                            st.rerun()

    # ── My orders tab ─────────────────────────────────────────────────────────
    with tab_orders:
        orders = get_user_orders(user["account_id"])
        total_qty = sum(o["quantity"] for o in orders)

        scol1, scol2 = st.columns(2)
        with scol1:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{len(orders)}</div><div class="stat-lbl">Total orders</div></div>', unsafe_allow_html=True)
        with scol2:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{total_qty:,}</div><div class="stat-lbl">Books ordered</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if not orders:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:var(--ink-3)">
              <div style="font-size:2.5rem">📦</div>
              <h3>No orders yet</h3>
              <p style="font-size:14px">Browse available books and place your first order.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            header = st.columns([1, 3, 1, 2, 2, 1])
            for col, label in zip(header, ["Order #", "Book", "Qty", "Location", "Date", ""]):
                col.markdown(f'<p style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)">{label}</p>', unsafe_allow_html=True)
            st.markdown('<hr style="border:none;border-top:1px solid var(--border);margin:0 0 .5rem">', unsafe_allow_html=True)

            for order in orders:
                row = st.columns([1, 3, 1, 2, 2, 1])
                row[0].markdown(f'<p style="color:var(--ink-2)"># {order["order_id"]}</p>', unsafe_allow_html=True)
                row[1].markdown(f'<p style="font-weight:500">{order["BookTitle"]}</p>', unsafe_allow_html=True)
                row[2].markdown(f'<p style="color:var(--ink-2)">{order["quantity"]:,}</p>', unsafe_allow_html=True)
                row[3].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{order["hall"]}, {order["building"]}</p>', unsafe_allow_html=True)
                row[4].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{order["order_date"]}</p>', unsafe_allow_html=True)
                with row[5]:
                    if st.button("Remove", key=f"remove_{order['item_id']}"):
                        success, msg = remove_order_item(order["item_id"])
                        set_toast(msg, "success" if success else "error")
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def screen_admin():
    user = st.session_state.user
    navbar(user["username"], "admin")

    st.markdown("""
    <div style="margin-bottom:1.5rem">
      <h2>Admin dashboard</h2>
      <p style="color:var(--ink-3);font-size:14px">Manage the book catalog and view all orders.</p>
    </div>
    """, unsafe_allow_html=True)

    show_toast()

    _, col_logout = st.columns([6, 1])
    with col_logout:
        if st.button("Sign out", key="admin_logout"):
            logout()
            st.rerun()

    tab_books, tab_orders, tab_add, tab_inv = st.tabs(["All books", "All orders", "Add book", "Inventory"])
    inject_tab_js(st.session_state.admin_tab)

    # ── All books tab ─────────────────────────────────────────────────────────
    with tab_books:
        books = get_all_books()

        fcol1, fcol2 = st.columns([2, 1])
        with fcol1:
            search = st.text_input("", placeholder="Search by title…", key="a_search", label_visibility="collapsed")
        with fcol2:
            categories = ["All categories"] + sorted(set(b["Category"] for b in books))
            cat_filter = st.selectbox("", categories, key="a_cat", label_visibility="collapsed")

        filtered = [
            b for b in books
            if (not search or search.lower() in b["Title"].lower())
            and (cat_filter == "All categories" or b["Category"] == cat_filter)
        ]

        st.markdown(f'<p style="font-size:12px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem">{len(filtered)} book{"s" if len(filtered) != 1 else ""}</p>', unsafe_allow_html=True)

        if not filtered:
            st.markdown('<div style="text-align:center;padding:3rem;color:var(--ink-3)"><div style="font-size:2.5rem">📚</div><h3>No books found</h3></div>', unsafe_allow_html=True)
        else:
            header = st.columns([3, 2, 1, 1, 3, 1])
            for col, label in zip(header, ["Title", "Category", "Year", "Pages", "Description", ""]):
                col.markdown(f'<p style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)">{label}</p>', unsafe_allow_html=True)
            st.markdown('<hr style="border:none;border-top:1px solid var(--border);margin:0 0 .5rem">', unsafe_allow_html=True)

            for book in filtered:
                row = st.columns([3, 2, 1, 1, 3, 1])
                row[0].markdown(f'<p style="font-weight:500">{book["Title"]}</p>', unsafe_allow_html=True)
                row[1].markdown(f'<span class="badge-amber">{book["Category"]}</span>', unsafe_allow_html=True)
                row[2].markdown(f'<p style="color:var(--ink-2)">{book["YearPublished"]}</p>', unsafe_allow_html=True)
                row[3].markdown(f'<p style="color:var(--ink-2)">{book["Pages"]:,}</p>', unsafe_allow_html=True)
                row[4].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{book.get("Description") or "—"}</p>', unsafe_allow_html=True)
                with row[5]:
                    if st.button("Delete", key=f"del_{book['book_id']}"):
                        success, msg = delete_book(book["book_id"])
                        set_toast(msg, "success" if success else "error")
                        st.rerun()

    # ── All orders tab ────────────────────────────────────────────────────────
    with tab_orders:
        orders = get_all_orders()
        customers = len(set(o["Customer"] for o in orders))
        total_qty = sum(o["quantity"] for o in orders)

        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{len(orders)}</div><div class="stat-lbl">Total orders</div></div>', unsafe_allow_html=True)
        with scol2:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{customers}</div><div class="stat-lbl">Customers</div></div>', unsafe_allow_html=True)
        with scol3:
            st.markdown(f'<div class="stat-card"><div class="stat-val">{total_qty:,}</div><div class="stat-lbl">Books ordered</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        ao_search = st.text_input("", placeholder="Search by customer or book…", key="ao_search", label_visibility="collapsed")

        filtered_orders = [
            o for o in orders
            if not ao_search
            or ao_search.lower() in o["Customer"].lower()
            or ao_search.lower() in o["BookTitle"].lower()
        ]

        if not filtered_orders:
            st.markdown('<div style="text-align:center;padding:3rem;color:var(--ink-3)"><div style="font-size:2.5rem">📦</div><h3>No orders found</h3></div>', unsafe_allow_html=True)
        else:
            header = st.columns([1, 2, 3, 1, 2, 2])
            for col, label in zip(header, ["Order #", "Customer", "Book", "Qty", "Location", "Date"]):
                col.markdown(f'<p style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)">{label}</p>', unsafe_allow_html=True)
            st.markdown('<hr style="border:none;border-top:1px solid var(--border);margin:0 0 .5rem">', unsafe_allow_html=True)

            for order in filtered_orders:
                row = st.columns([1, 2, 3, 1, 2, 2])
                row[0].markdown(f'<p style="color:var(--ink-2)">#{order["order_id"]}</p>', unsafe_allow_html=True)
                row[1].markdown(f'<span class="badge-gray">{order["Customer"]}</span>', unsafe_allow_html=True)
                row[2].markdown(f'<p style="font-weight:500">{order["BookTitle"]}</p>', unsafe_allow_html=True)
                row[3].markdown(f'<p style="color:var(--ink-2)">{order["quantity"]:,}</p>', unsafe_allow_html=True)
                row[4].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{order["hall"]}, {order["building"]}</p>', unsafe_allow_html=True)
                row[5].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{order["order_date"]}</p>', unsafe_allow_html=True)

    # ── Add book tab ──────────────────────────────────────────────────────────
    with tab_add:
        st.markdown('<h3 style="margin-bottom:1.25rem">Add a new book</h3>', unsafe_allow_html=True)

        with st.form("add_book_form"):
            ab_title = st.text_input("Title", placeholder="Book title")
            acol1, acol2 = st.columns(2)
            with acol1:
                ab_cat   = st.text_input("Category", placeholder="e.g. Fiction")
                ab_year  = st.number_input("Year published", min_value=1000, max_value=2100, value=2024)
            with acol2:
                ab_pages = st.number_input("Pages", min_value=1, value=100)
            ab_desc  = st.text_area("Description", placeholder="Brief description of the book…", height=100)

            _, bcol2 = st.columns([1, 1])
            with bcol2:
                submitted = st.form_submit_button("Add book", use_container_width=True)
            if submitted:
                if not ab_title or not ab_cat:
                    set_toast("Fill in all required fields.", "error")
                    st.rerun()
                else:
                    success, msg = add_book(int(ab_year), ab_title, ab_desc, ab_cat, int(ab_pages))
                    set_toast(msg, "success" if success else "error")
                    st.rerun()

    # ── Inventory tab ─────────────────────────────────────────────────────────
    with tab_inv:
        st.markdown('<h3 style="margin-bottom:1.25rem">Manage inventory</h3>', unsafe_allow_html=True)

        # Add to inventory form
        with st.expander("Add book to inventory", expanded=False):
            books   = get_all_books()
            shelves = get_all_shelves()

            with st.form("inv_add_form"):
                book_options  = {f"{b['Title']} ({b['Category']})": b["book_id"] for b in books}
                shelf_options = {f"{s['hall']}, {s['building']} — Floor {s['floor']}": s["shelf_id"] for s in shelves}

                selected_book  = st.selectbox("Book", list(book_options.keys()), key="inv_book")
                selected_shelf = st.selectbox("Shelf", list(shelf_options.keys()), key="inv_shelf")
                inv_qty = st.number_input("Quantity", min_value=1, value=1, key="inv_qty")

                if st.form_submit_button("Add to inventory", use_container_width=True):
                    success, msg = add_to_inventory(
                        book_options[selected_book],
                        shelf_options[selected_shelf],
                        int(inv_qty)
                    )
                    set_toast(msg, "success" if success else "error")
                    set_active_tab(3)
                    st.rerun()

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # Current inventory table
        inventory = get_inventory()
        if not inventory:
            st.markdown('<div style="text-align:center;padding:3rem;color:var(--ink-3)"><div style="font-size:2.5rem">📦</div><h3>No inventory</h3><p style="font-size:14px">Add books above to make them available for ordering.</p></div>', unsafe_allow_html=True)
        else:
            header = st.columns([3, 2, 2, 2, 1, 1])
            for col, label in zip(header, ["Title", "Category", "Location", "Qty", "", ""]):
                col.markdown(f'<p style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)">{label}</p>', unsafe_allow_html=True)
            st.markdown('<hr style="border:none;border-top:1px solid var(--border);margin:0 0 .5rem">', unsafe_allow_html=True)

            for item in inventory:
                with st.form(key=f"inv_row_{item['item_id']}"):
                    row = st.columns([3, 2, 2, 2, 1, 1])
                    row[0].markdown(f'<p style="font-weight:500">{item["Title"]}</p>', unsafe_allow_html=True)
                    row[1].markdown(f'<span class="badge-amber">{item["Category"]}</span>', unsafe_allow_html=True)
                    row[2].markdown(f'<p style="font-size:13px;color:var(--ink-3)">{item["Hall"]}, {item["Building"]}</p>', unsafe_allow_html=True)
                    with row[3]:
                        new_qty = st.number_input("", min_value=0, value=int(item["quantity"]),
                                                  key=f"inv_edit_{item['item_id']}", label_visibility="collapsed")
                    with row[4]:
                        if st.form_submit_button("Update"):
                            success, msg = update_inventory_quantity(item["item_id"], new_qty)
                            set_toast(msg, "success" if success else "error")
                            set_active_tab(3)
                            st.rerun()
                    with row[5]:
                        if st.form_submit_button("Remove"):
                            success, msg = remove_from_inventory(item["item_id"])
                            set_toast(msg, "success" if success else "error")
                            set_active_tab(3)
                            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.user:
    screen_auth()
else:
    st.markdown("""
    <style>
    .block-container {
      background: #fff;
      border-radius: 12px;
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      padding: 2rem 2.5rem !important;
      margin-top: 1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    user = st.session_state.user
    if user.get("role") == "admin":
        screen_admin()
    else:
        screen_user()
