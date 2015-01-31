describe('Reader page tests', function() {
  it('should have correct title', function() {
    browser.get('http://localhost:8000');

    expect(browser.getTitle()).toBe("ThirdDime - Explore art through interpretations and stories");
  });
});