


def get_family_tree(child):
  subcategories = child.subcategories.all()
  if not subcategories:
      return {
        "title": child.title, 
        "slug":child.slug,
        "items_count":"",
        "subcategories": []
      }
  return {
      "title": child.title,
      "slug":child.slug,
      "subcategories": [get_family_tree(child) for child in subcategories],
  }


def get_subcategories_count(child):
  subcategories = child.subcategories.all()
  if not subcategories:
      return {
        "title": child.title, 
        "slug":child.slug,
        "items_count":"",
        "subcategories": []
      }
  return {
      "title": child.title,
      "slug":child.slug,
      "subcategories": [get_family_tree(child) for child in subcategories],
  }
