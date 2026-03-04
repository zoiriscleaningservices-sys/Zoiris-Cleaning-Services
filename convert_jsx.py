import re

def convert_html_to_jsx(html_content):
    # Rip out scripts and styles to prevent JSX compilation errors
    jsx = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    jsx = re.sub(r'<style.*?>.*?</style>', '', jsx, flags=re.DOTALL | re.IGNORECASE)
    
    # Strip comments completely to avoid weird { /* */ } nesting issues
    jsx = re.sub(r'<!--.*?-->', '', jsx, flags=re.DOTALL)
    
    # Basic JSX conversions
    jsx = jsx.replace('class=', 'className=')
    jsx = jsx.replace('for=', 'htmlFor=')
    jsx = jsx.replace('tabindex=', 'tabIndex=')
    jsx = jsx.replace('autocomplete=', 'autoComplete=')
    jsx = jsx.replace('stroke-linecap=', 'strokeLinecap=')
    jsx = jsx.replace('stroke-linejoin=', 'strokeLinejoin=')
    jsx = jsx.replace('stroke-width=', 'strokeWidth=')
    jsx = jsx.replace('required=""', 'required')
    jsx = jsx.replace('allowfullscreen=""', 'allowFullScreen')
    jsx = jsx.replace('referrerpolicy=', 'referrerPolicy=')
    jsx = re.sub(r'maxlength="(\d+)"', r'maxLength={\1}', jsx, flags=re.IGNORECASE)
    jsx = re.sub(r'rows="(\d+)"', r'rows={\1}', jsx, flags=re.IGNORECASE)
    jsx = re.sub(r'cols="(\d+)"', r'cols={\1}', jsx, flags=re.IGNORECASE)
    
    # Handle inline JS events (React requires functions, vanilla uses strings which crash the build)
    jsx = re.sub(r'onsubmit="[^"]*"', 'onSubmit={(e) => e.preventDefault()}', jsx, flags=re.IGNORECASE)
    # Strip all remaining on... attributes like onmouseover, onmouseout, onclick
    jsx = re.sub(r'\bon[a-z]+="[^"]*"', '', jsx, flags=re.IGNORECASE)
    
    jsx = jsx.replace('disabled selected>', 'disabled>')
    
    # Close unclosed tags
    tags_to_close = ['img', 'br', 'hr', 'input', 'meta', 'link']
    for tag in tags_to_close:
        # Match e.g. <img src="a.jpg"> and make it <img src="a.jpg" />
        jsx = re.sub(rf'<({tag}[^>]*?)(?<!/)>', rf'<\1 />', jsx, flags=re.IGNORECASE)
        
    # Strip inline styles as they cause dictionary issues in React (style="color:red")
    jsx = re.sub(r'style="[^"]*"', '', jsx, flags=re.IGNORECASE)
    
    return jsx

if __name__ == "__main__":
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        body_content = html
        
    jsx_content = convert_html_to_jsx(body_content)
    
    component = """
export default function Home() {
  return (
    <>
""" + jsx_content + """
    </>
  );
}
"""
    with open("app/page.tsx", "w", encoding="utf-8") as f:
        f.write(component)
    
    print("Successfully converted index.html to valid app/page.tsx")
