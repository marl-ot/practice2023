from flask import render_template, send_file


def iframe_injection_page(request):
    iframe_url = request.args.get('page')
    return render_template("iframe_injection/iframe_injection.html", iframe_url=iframe_url)