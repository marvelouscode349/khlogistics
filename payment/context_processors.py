# context processors for making payments url available

def exempted_urls(request):
    # Define your list of exempted URLs
    exempted_urls_list = ['/payment/make', '/payment/confirm', '/payment/success']

    # Return the exempted URLs as a dictionary
    return {'exempted_urls': exempted_urls_list}
