import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = [ "faqItem" ]

    toggle(event) {
        event.currentTarget.classList.toggle('active');
    }
}