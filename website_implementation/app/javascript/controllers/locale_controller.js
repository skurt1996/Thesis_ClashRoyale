import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = [ "localeItem" ]

    changeLocale(event) {
        const locale = event.target.id;
        window.location.href = `${window.location.pathname}?locale=${locale}`;
    }
}