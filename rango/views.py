from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

# a simple test view
def index(request):
    # Request the context of the HTTP request.
    # The context contains the information such as the client's machine details
    context = RequestContext(request)
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary which will be passed to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned adn craete a URL attribute
    # This attribute stores an encoded URL(e.g. Spaces replaced with underscores.
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    #context_dict = {'boldmessage': "I am bold font from the context"}

    pages_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = pages_list


    #Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)
    # return HttpResponse("Rango says hello world! <a href='/rango/about'>About</a>")



# a new view called about which returns:
# Rango Says: Here is the about page
def about(request):
    context = RequestContext(request)
    context_dict = {'aboutmessage': "I am the About message from the context"}
    return render_to_response('rango/about.html', context_dict, context)


    # return HttpResponse("Rango Says: Here is the about page. <a href='/rango/'>Index</a>")


# A new view!
def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores
    # We can then replace the underscores with spaces to get the name.
    # category_name = category_name_url.replace('_', ' ')
    category_name = decode_url(category_name_url)

    # Create a context dictionary which we can pass to the template
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

    try:
        #Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception
        # So the .get() method returns one model instance or raises an exception
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # NOte that filter returns >= 1 model instance
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context under name pages
        context_dict['pages'] = pages
        #We also add the category object from the database to the context dictionary
        # We'll use this in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        # Don't do anything - the the template displays the "no category" message for us
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/category.html', context_dict, context)


def decode_url(x):
    return x.replace('_', ' ')



def add_category(request):
    #Get the context fom the request.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided a valid form?
        if form.is_valid():
            # Save the new category to the databse.
            form.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors so print them
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error message (is any).
    return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category exists
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # Go back and render the add category form
                return render_to_response('rango/add_category.html', {}, context)
            #Also create a default value for the number of views.
            page.views = 0

            # Now save the new model instance.
            page.save()

            #Now that the page is saved, display the category instead.
            return category(request, category_name_url)

        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',
        {'category_name_url': category_name_url,
         'category_name': category_name, 'form': form},
         context)