describe('Reader page tests', function() {

    beforeEach(function () {
        browser.get("http://localhost:8000");
    });

    it('should have correct title', function() {
        expect(browser.getTitle()).toBe("ThirdDime - Explore art through interpretations and stories");
    });

    it("should have a correct title", function () {
        var mainHeader = element.all((by.tagName("h1")));
        expect(mainHeader.count()).toBe(0);
        expect(mainHeader.first().getText()).toBe("ThirdDime");
    });

    it("should have hot as default stream", function () {
        var streams = element(by.css(".streams"));
        var defaultStream = streams.element(by.css(".active"));

        expect(defaultStream.getText()).toBe("Hot");
    });
    xit("should give a list of hot images");
    xit("when latest is selected should give list of latest image");
    xit("when trending is selected should give list of trending image");
    xit("should load more paintings when bottom of the page is hit");
    xit("should show name of the painting as the title");
    xit("should show interpretation on the painting");
    xit("should show description of painting in case interpretation is not present");
    xit("should take user to painting page in new tab on clicking a painting");
});