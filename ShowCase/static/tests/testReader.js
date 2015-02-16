describe('Reader page tests', function() {
    // ==================================
    // Starting tests for Reader. Please make sure test user is created.
    // ==================================

    beforeEach(function () {
        browser.get("http://localhost:8000");
    });

    it('should have correct title', function() {
        expect(browser.getTitle()).toBe("ThirdDime - Explore art through interpretations and stories");
    });

    it("should have a correct title", function () {
        var mainHeader = element.all((by.tagName("h1")));
        expect(mainHeader.count()).toBe(1);
        expect(mainHeader.first().getText()).toBe("ThirdDime");
    });

    it("User is able to login", function () {
        // Ensure a non- authenticated user
        // else next step fails.

        // Tesla visits reader page and notices login anchor.
        var login_anchor  = element(by.css(".auth-user"));
        expect(login_anchor.getText()).toBe("Login");

        // He clicks on the login button and login form opens.
        login_anchor.click();
        browser.driver.sleep(400);
        var login_with_facebook = element(by.css(".curtain-right .social .facebook")).isDisplayed();
        expect(login_with_facebook).toBeTruthy();

        // He enters his email and usrename, then clicks login.
        var email_field = element(by.css(".curtain-right .native input[type='email']")).sendKeys("rohit@user.com");
        var password_field = element(by.css(".curtain-right .native input[type='password']")).sendKeys("rohit");
        var login_button = element(by.css(".curtain-right .native . login_button")).click;

        //Page reloads to show name of the user rather than login button
        expect(login_anchor.isPresent()).toBeFalsy();

        //May be some other way of validating that the user is logged in, like some REST API.
    });

    /*it("should have hot as default stream", function () {
        var streams = element(by.css(".streams"));
        var defaultStream = streams.element(by.css(".active"));

        expect(defaultStream.getText()).toBe("Hot");
    });*/
    xit("should give a list of hot images");
    xit("when latest is selected should give list of latest image");
    xit("when trending is selected should give list of trending image");
    xit("should load more paintings when bottom of the page is hit");
    xit("should show name of the painting as the title");
    xit("should show interpretation on the painting");
    xit("should show description of painting in case interpretation is not present");
    xit("should take user to painting page in new tab on clicking a painting");
});