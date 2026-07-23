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

Backend: FastAPI + Supabase (Postgres)



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
