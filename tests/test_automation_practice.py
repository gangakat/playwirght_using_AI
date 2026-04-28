from typing import List

from playwright.sync_api import Page, expect


def accept_alert(page: Page) -> List[str]:
    messages = []
    page.once("dialog", lambda dialog: (messages.append(dialog.message), dialog.accept()))
    return messages


# Positive scenarios


def test_positive_page_title_and_heading_load(page: Page) -> None:
    expect(page).to_have_title("Practice Page")
    expect(page.get_by_role("heading", name="Practice Page")).to_be_visible()


def test_positive_select_radio_button(page: Page) -> None:
    page.locator("input[value='radio2']").check()
    expect(page.locator("input[value='radio2']")).to_be_checked()


def test_positive_autocomplete_country_suggestion(page: Page) -> None:
    page.locator("#autocomplete").fill("Ind")
    page.get_by_text("India", exact=True).click()
    expect(page.locator("#autocomplete")).to_have_value("India")


def test_positive_dropdown_option_selection(page: Page) -> None:
    page.locator("#dropdown-class-example").select_option("option2")
    expect(page.locator("#dropdown-class-example")).to_have_value("option2")


def test_positive_multiple_checkboxes_can_be_selected(page: Page) -> None:
    page.locator("#checkBoxOption1").check()
    page.locator("#checkBoxOption3").check()
    expect(page.locator("#checkBoxOption1")).to_be_checked()
    expect(page.locator("#checkBoxOption3")).to_be_checked()


def test_positive_alert_displays_entered_name(page: Page) -> None:
    messages = accept_alert(page)
    page.locator("#name").fill("John Doe")
    page.locator("#alertbtn").click()
    assert messages == ["Hello John Doe, share this practice page and share your knowledge"]


def test_positive_confirm_dialog_can_be_accepted(page: Page) -> None:
    messages = accept_alert(page)
    page.locator("#name").fill("John Doe")
    page.locator("#confirmbtn").click()
    assert messages == ["Hello John Doe, Are you sure you want to confirm?"]


def test_positive_hide_and_show_textbox(page: Page) -> None:
    text_box = page.locator("#displayed-text")
    page.locator("#hide-textbox").click()
    expect(text_box).to_be_hidden()
    page.locator("#show-textbox").click()
    expect(text_box).to_be_visible()


def test_positive_web_table_contains_expected_course(page: Page) -> None:
    row = page.locator("#product tr").filter(has_text="Master Selenium Automation in simple Python Language")
    expect(row).to_contain_text("Rahul Shetty")
    expect(row).to_contain_text("25")


def test_positive_iframe_courses_are_visible(page: Page) -> None:
    frame = page.frame_locator("#courses-iframe")
    expect(frame.locator("body")).to_contain_text("Courses")


# Negative scenarios


def test_negative_radio_buttons_are_not_preselected(page: Page) -> None:
    expect(page.locator("input[value='radio1']")).not_to_be_checked()
    expect(page.locator("input[value='radio2']")).not_to_be_checked()
    expect(page.locator("input[value='radio3']")).not_to_be_checked()


def test_negative_unselected_radio_remains_unchecked(page: Page) -> None:
    page.locator("input[value='radio1']").check()
    expect(page.locator("input[value='radio2']")).not_to_be_checked()


def test_negative_dropdown_placeholder_is_default(page: Page) -> None:
    expect(page.locator("#dropdown-class-example")).to_have_value("")


def test_negative_checkboxes_are_not_checked_by_default(page: Page) -> None:
    expect(page.locator("#checkBoxOption1")).not_to_be_checked()
    expect(page.locator("#checkBoxOption2")).not_to_be_checked()
    expect(page.locator("#checkBoxOption3")).not_to_be_checked()


def test_negative_unchecked_checkbox_stays_unchecked(page: Page) -> None:
    page.locator("#checkBoxOption2").check()
    expect(page.locator("#checkBoxOption1")).not_to_be_checked()
    expect(page.locator("#checkBoxOption3")).not_to_be_checked()


def test_negative_alert_empty_name_is_not_personalized(page: Page) -> None:
    messages = accept_alert(page)
    page.locator("#alertbtn").click()
    assert messages == ["Hello , share this practice page and share your knowledge"]


def test_negative_confirm_empty_name_is_not_personalized(page: Page) -> None:
    messages = accept_alert(page)
    page.locator("#confirmbtn").click()
    assert messages == ["Hello , Are you sure you want to confirm?"]


def test_negative_hidden_textbox_cannot_be_seen(page: Page) -> None:
    page.locator("#hide-textbox").click()
    expect(page.locator("#displayed-text")).not_to_be_visible()


def test_negative_missing_course_is_absent_from_table(page: Page) -> None:
    expect(page.locator("table.table-display")).not_to_contain_text("Imaginary Playwright Course")


def test_negative_broken_link_is_detected(page: Page) -> None:
    broken_link = page.get_by_role("link", name="Broken Link")
    expect(broken_link).to_have_attribute("href", "https://rahulshettyacademy.com/brokenlink")
    href = broken_link.get_attribute("href")
    assert href is not None
    response = page.request.get(href)
    assert response.status >= 400


# Edge cases


def test_edge_autocomplete_keeps_unknown_country_text(page: Page) -> None:
    page.locator("#autocomplete").fill("Atlantis")
    expect(page.locator("#autocomplete")).to_have_value("Atlantis")
    expect(page.locator(".ui-menu-item")).to_have_count(0)


def test_edge_alert_accepts_special_characters(page: Page) -> None:
    value = "QA User !@#$%"
    messages = accept_alert(page)
    page.locator("#name").fill(value)
    page.locator("#alertbtn").click()
    assert messages == [f"Hello {value}, share this practice page and share your knowledge"]


def test_edge_table_price_total_matches_fixed_header_total(page: Page) -> None:
    amounts = page.locator("div.tableFixHead tbody tr td:nth-child(4)").all_inner_texts()
    calculated_total = sum(int(amount) for amount in amounts)
    displayed_total = page.locator(".totalAmount").inner_text()
    assert calculated_total == 296
    assert displayed_total.endswith(str(calculated_total))


def test_edge_mouse_hover_top_link_scrolls_to_top(page: Page) -> None:
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.locator("#mousehover").hover()
    page.get_by_role("link", name="Top").click()
    page.wait_for_function("window.scrollY === 0")
    assert page.evaluate("window.scrollY") == 0


def test_edge_new_tab_opens_with_expected_site(page: Page) -> None:
    with page.expect_popup() as popup_info:
        page.locator("#opentab").click()
    new_page = popup_info.value
    new_page.wait_for_load_state("domcontentloaded")
    assert "qaclickacademy.com" in new_page.url
    new_page.close()
