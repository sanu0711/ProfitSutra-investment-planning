document.addEventListener("DOMContentLoaded", () => {
    const spinner = document.getElementById("loading-spinner");
    const links = document.querySelectorAll("a");
    const forms = document.querySelectorAll("form");

    const hideSpinner = () => {
      if (spinner) {
        spinner.classList.add("d-none");
      }
    };

    const showSpinner = () => {
      if (spinner) {
        spinner.classList.remove("d-none");
      }
    };

    links.forEach(link => {
      link.addEventListener("click", event => {
        const href = link.getAttribute("href");

        if (href && !href.startsWith("#") && !link.target) {
          event.preventDefault();
          showSpinner();
          setTimeout(() => {
            window.location.href = href;
          }, 300); 
        }
      });
    });

    forms.forEach(form => {
      form.addEventListener("submit", () => {
        showSpinner();
      });
    });

    window.addEventListener("load", () => {
      hideSpinner();
    });


    window.addEventListener("pageshow", () => {
      hideSpinner();
    });

    window.addEventListener("popstate", () => {
      setTimeout(() => {
        hideSpinner();
      }, 300);  
    });

   
    hideSpinner();
  });