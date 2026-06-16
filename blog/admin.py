from django.contrib import admin
from django.contrib.auth.models import User

from .models import Comment, Post

# admin.site.register(Post)
admin.site.register(Comment)


# 1. Define the Inline class for the child model
class CommentInline(admin.StackedInline):  # Alternatively:
    # class CommentInline(admin.TabularInline):  # Alternatively: admin.StackedInline
    model = Comment
    extra = 1  # The number of empty forms to display at the bottom


# 2. Attach the Inline to the parent model's Admin class
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Changes the columns shown in the list view
    list_display = ("title", "author", "status", "created_on")

    # Adds a filter sidebar on the right
    list_filter = ("tags", "status", "created_on", "author")

    # Adds a search bar at the top (searches these specific fields)
    search_fields = ["title", "content"]
    # Register the inline here
    inlines = [CommentInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 1. Target the specific field we want to restrict
        if db_field.name == "author":
            # 2. Check if the logged-in user is NOT a superuser

            # 3. Force the dropdown choices to ONLY include the current user
            kwargs["queryset"] = User.objects.filter(id=request.user.id)

        # Pass the modified arguments back to the parent class method
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Automatically populates the slug based on the title (if you add a slug field later)
    # prepopulated_fields = {'slug': ('title',)}


# Note: We can remove admin.site.register(Comment) if we only want to
# manage comments directly from the Post page.
