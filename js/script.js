(() => {
  let pathEnding =
    window.location.pathname.split("/")[
      window.location.pathname.split("/").length - 1
    ];
  if (pathEnding.toLowerCase().replace(".html", "") === "faq") {
    document.getElementById("navbar-faq").classList.add("active");
    document.getElementById("navbar-faq").setAttribute("aria-current", "page");
  } else {
    document.getElementById("navbar-docs").classList.add("active");
    document.getElementById("navbar-docs").setAttribute("aria-current", "page");
  }

  let onResize = (media) => {
    let sidebarMenu = document.getElementById("sidebarMenu");

    if (media.matches) {
      document.getElementsByTagName("main")[0].style.marginLeft =
        sidebarMenu.getBoundingClientRect().width * 1.15 + "px";
      document.getElementsByTagName("main")[0].style.marginRight =
        sidebarMenu.getBoundingClientRect().width * 0.15 + "px";
      document.getElementsByTagName("header")[0].style.marginLeft =
        sidebarMenu.getBoundingClientRect().width * 1.15 + "px";
    } else {
      document.getElementsByTagName("header")[0].style.marginLeft = "";
      document.getElementsByTagName("main")[0].style.marginLeft = "";
      document.getElementsByTagName("main")[0].style.marginRight = "";
    }
  };
  let onResizeMedia = window.matchMedia("(min-width: 768px)");
  onResize(onResizeMedia);
  onResizeMedia.addListener(onResize);

  let onThemeChange = () => {
    if (document.querySelector("[href$='/css/highlightjs/ayu-highlight.css']").hasAttribute('disabled')) {
      document.querySelector("[href$='/css/highlightjs/ayu-highlight.css']").removeAttribute('disabled');
    } else if (document.querySelector("[href$='/css/highlightjs/highlight.css']").hasAttribute('disabled')) {
      document.querySelector("[href$='/css/highlightjs/highlight.css']").removeAttribute('disabled');
    }
    if (!document.querySelector("[data-bs-theme=dark] [href$='/css/highlightjs/ayu-highlight.css']")) {
      document.querySelector("[href$='/css/highlightjs/ayu-highlight.css']").setAttribute('disabled', '');
    } else {
      document.querySelector("[href$='/css/highlightjs/highlight.css']").setAttribute('disabled', '');
    }
  }
  onThemeChange();
  document.querySelectorAll("button.dropdown-item.d-flex.align-items-center").forEach((element) => {
    element.addEventListener('click', () => {
      setTimeout(onThemeChange, 0);
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) {
      return;
    }
    if (window.search && window.search.hasFocus()) {
      return;
    }

    let active = document.querySelector("li > .nav-link.active").parentElement;
    if (e.key === 'ArrowLeft') {
      let previous = active.previousElementSibling;
      while (previous && previous.classList.contains("sidebar-header")) {
        previous = previous.previousElementSibling;
      }
      if (previous) {
        e.preventDefault();
        previous.children[0].click();
      }
    } else if (e.key === 'ArrowRight') {
      let next = active.nextElementSibling;
      while (next && next.classList.contains("sidebar-header")) {
        next = next.nextElementSibling;
      }
      if (next) {
        e.preventDefault();
        next.children[0].click();
      }
    }
  });

  const tooltipTriggerList = Array.from(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.forEach((tooltipTriggerEl) => {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Syntax highlighting Configuration
  hljs.configure({
    tabReplace: "    ", // 4 spaces
    languages: [], // Languages used for auto-detection
  });

  let code_nodes = Array.from(document.querySelectorAll("code"))
    // Don't highlight `inline code` blocks in headers.
    .filter(function (node) {
      return !node.parentElement.classList.contains("header");
    });
  code_nodes.forEach(function (block) {
    hljs.highlightBlock(block);
  });
  // Adding the hljs class gives code blocks the color css
  // even if highlighting doesn't apply
  code_nodes.forEach(function (block) {
    block.classList.add("hljs");
  });
})();
