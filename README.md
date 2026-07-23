LAAM — Purchase Confidence

A small full-stack experience that helps a customer make a confident purchase decision for a fashion product size availability, transparent pricing, delivery estimates, and alternatives, all on one page.

1. Problem Understanding

    The main problem in this is that the customer found the product they like but they hesitate before adding it in cart due to some uncertainties like: is the product of their desired size in stock, are there any hidden charges that are not mentioned with the product but will show up on checkout, will the product be delivered to their location, and if the product is not in their desired size or quantity do they have alternatives.

    As I myself do a lot of online shopping, this problem is one of the main problems while ordering online sometimes at the checkout time I got to know that there are some more hidden charges like tax, or sometimes that particular brand doesn't deliver to my location.

    So as a victim of this very same problem, I always think of the solution that all these things should be mentioned before the customer adds that product to the cart because if the person faces such issues after adding to the cart, it loses its interest in that shopping site.

2. Scope

What I built:

    The solution that was in my mind is that when the customer is interested in a particular product and clicks on that product and the product page is opened, all these problems should be solved there.

    1. Starting with the size: All the available sizes should be mentioned and the ones that are not available should be highlighted. Then when clicking any size, its stock should be mentioned like in stock, out of stock, or limited stock. For this we can set threshold values if stock < 3 then limited stock, and so on. This will solve the customer's problem of whether stock is available for their desired size.

    Here we can add that when the product is out of stock, some alternative products of the same category and price range should be suggested (it can also be made general, like a bar that always appears containing alternative products).

    2. Next, the payment part: There should be a detailed price breakdown with the product, like:

    What is the base price of the product?
    If there are any discounts?
    Any tax?

    And then the final price of the product should be mentioned there.

    3. Third is the delivery location issue: An option to enter the pin code of the customer's area that will tell if delivery is available there, and an approximated time of delivery.

    What I didn't build:

    I just focused on solving the issues that were mentioned in the problem statement I didn't make the cart page or the checkout page. And as I am using seed data, the alternatives part is not done as it should be, as it depends on category of the product and the price range of the product rather than an recommendation model, and as for my database schema, it is simple for now, which can be changed in the future.


3. User Flow

For the user flow, it is like:

    1.The first page I build is the products page. The user clicks their desired product.
    2.On clicking it, it navigates to the product view page.
    3.Customer selects a size the page fetches live stock status for that size and outputs there.
    4.For the out-of-stock case, some alternative products with the same category and price range are displayed at  the bottom of the page.
    5.Next, below it, there is a price breakdown and then a total price that the customer will pay for the product.
    6.For delivery options, the customer types the pin code of their location the page shows an estimated delivery window and date for that pin code, or a clear "not serviceable here" message if it's out of range.


4. Technical Approach

Frontend: Next.js 14 (App Router) + TypeScript + Tailwind

frontend/
├── app/
│   ├── page.tsx                     # the products listing page
│   ├── product/[id]/page.tsx        # the actual product page fetches the product on the
│   └── product/[id]/not-found.tsx   # shown if someone opens a product id that doesn't exist
├── components/
│   ├── ProductView.tsx               # this is the main component that contain all product details
│   ├── SizeSelector.tsx              # the clickable size chips
│   ├── StockBadge.tsx                # shows in stock / limited stock / out of stock with a color next to it
│   ├── PriceBreakdown.tsx            # base price, discounts, fees, final price
│   ├── DeliveryEstimate.tsx          # the pincode input and result
│   ├── AlternativesGrid.tsx          # only shows up when the selected size is out of stock
│   └── LoadingSkeleton.tsx / ErrorState.tsx   # small reusable pieces so every section can
│                                     # show its own loading/error state instead of the whole
│                                     # page breaking if one part fails
├── hooks/
│   ├── useAvailability.ts            # runs the stock check whenever the selected size
│   │                                 # changes, and ignores the result if the user has
│   │                                 # already switched to a different size before it comes
│   │                                 # back (so an old slow response can't overwrite a newer
│   │                                 # one)
│   └── useDeliveryEstimate.ts        # waits 400ms after the user stops typing the pincode
│                                     # before actually calling the API, so it's not sending a
│                                     # request on every single keystroke
└── lib/
    ├── api.ts                        # all the fetch calls to the backend live here, with one
    │                                 # shared error type so I'm not handling errors
    │                                 # differently in every component
    └── types.ts                     # the TypeScript types, written to match the backend's
                                      # response shapes exactly


Data Model 
products (id, title, brand, category, base_price, image_url) 
    └─ product_variants (product_id, size, stock_qty) 
    └─ price_adjustments (product_id, label, type[discount|fee], amount, is_percentage) 
delivery_zones (pincode_prefix, min_days, max_days, is_serviceable)


Backend: FastAPI + Supabase (Postgres)


backend/
├── main.py                   # this is where the app actually starts sets up CORS so the
│                             # frontend is allowed to call it, registers all the routers,
│                             # and has a simple /health route just to check the server is alive
|
├── config.py                 # all the settings in one place the database URL, which
│                             # frontend origin is allowed to call the API, the stock
│                             # threshold, and the price tolerance used for alternatives
|
├── db.py                     # sets up the async SQLAlchemy connection to Supabase
|
├── schema.sql                # the table definitions I run this once manually in the
│                             # Supabase SQL editor, it's not run automatically by the app
|
├── seed.sql                  # fake product/stock/price/delivery data so there's something
│                             # to actually test the UI states with 
|
├── routers/                  # these files only handle the request/response part they
│   │                         # don't calculate anything themselves, they just call the
│   │                         # service functions and return the result
|   |
│   ├── products.py           # GET /products and GET /products/{id}
|   |
│   ├── availability.py       # GET /products/{id}/availability?size=
|   |
│   ├── delivery.py           # GET /delivery/estimate?pincode=&product_id=
|   |
│   └── alternatives.py       # GET /products/{id}/alternatives?exclude_size=
|  
├── repositories/             # this is the layer that actually talks to the database 
│                             # writes the SQLAlchemy queries, nothing else
|
├── services/                 # this is the important folder plain Python functions with
│   │                         # no FastAPI or database code in them at all, just the actual
│   │                         # logic, so I can test them directly
|   |
│   ├── pricing.py            # takes base price + list of discounts/fees and works out the
│   │                         # final price: discounts are applied first, then fees, so the
│   │                         # fee doesn't get calculated on the original price by mistake
|   |
│   ├── availability.py       # takes a stock number and decides if it's in stock / limited
│   │                         # stock / out of stock, based on the threshold from config.py
|   |
│   ├── delivery.py           # takes a pincode and the list of delivery zones and figures
│   │                         # out if we deliver there and how long it'll take
|   |
│   └── matching.py           # the alternatives logic same category, price within range,
│                             # and the size the customer wanted has to actually be in stock
|
├── schemas/                  # these are just the Pydantic models that define what the API
│                             # response looks like 


__________________________________________________________________________________________________________
| Method |	 Path	                                              | Purpose                              |
|_________________________________________________________________|______________________________________|
| GET	 |  /products	                                          | Catalog listing                      |
| GET	 |  /products/{id}	                                      | Product + variants + price breakdown |
| GET	 |  /products/{id}/availability?size=M	                  | Stock status for one size            | 
| GET	 |  /delivery/estimate?pincode=54000&product_id={id}	  | Delivery window, or "unavailable"    |
| GET	 |  /products/{id}/alternatives?exclude_size=M	          | Similar in-stock alternatives        |
| GET	 |  /health	                                              | Liveness check                       |
|_________________________________________________________________|______________________________________|





5. How to Run

Clone the repository

git clone https://github.com/maheen-zahid-26/LAAM-Assessment.git
cd LAAM-Assessment

Database setup (one-time only)

This project uses Supabase (Postgres). If you're connecting to a fresh
Supabase project that doesn't have these tables yet, paste the contents of
backend/schema.sql, then backend/seed.sql, into the Supabase SQL editor.
This only needs to be done once per project — the data persists, so you
don't repeat this step on every run.

Backend

cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
make a .env file in the backend folder and paste
	
	DATABASE_URL=postgresql+asyncpg://postgres.tmbhfuywlickbsepbxya:cQW%40b2%3F%40yK7FHcw@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres

	CORS_ORIGIN=http://localhost:3000

uvicorn main:app --reload --port 8000

Backend runs at http://localhost:8000 — API docs at http://localhost:8000/docs

Frontend

cd frontend
npm install
npm run dev

Note: start the backend before the frontend.


