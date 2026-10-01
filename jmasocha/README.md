# J Masocha Photography — website redesign

Static redesign of www.jmasochaphoto.co.za: Home, Services, Gallery, Printing, About and Contact.
No WordPress, plugins or database; it runs on any static host.

## Editing

All page content lives in `build.py` (services, gallery photos and categories, products, team, reviews, FAQ).
Edit it and run `python3 build.py` to regenerate the HTML (needs `pip install pillow`).

### Adding a gallery photo
1. Export two WebP sizes into `assets/img/gallery/`: `<name>-700.webp` and `<name>-1600.webp`.
2. Add a line to `GALLERY` in `build.py` with the name, alt text, caption and categories
   (`kids women men couples family maternity graduation birthdays outdoor`).
3. Run `python3 build.py`. Filter counts update automatically.

## Bookings
The contact form and every "Request packages" button open WhatsApp (066 132 2462) or the visitor's
email app with the details filled in, so no server is needed.
