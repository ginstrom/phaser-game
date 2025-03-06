import { TextStyles } from '../../ui/TextStyles';

describe('TextStyles', () => {
  it('should export title style', () => {
    expect(TextStyles.title).toBeDefined();
    expect(TextStyles.title.fontSize).toBeDefined();
    expect(TextStyles.title.fontFamily).toBeDefined();
    expect(TextStyles.title.color).toBeDefined();
  });

  it('should export subtitle style', () => {
    expect(TextStyles.subtitle).toBeDefined();
    expect(TextStyles.subtitle.fontSize).toBeDefined();
    expect(TextStyles.subtitle.fontFamily).toBeDefined();
    expect(TextStyles.subtitle.color).toBeDefined();
  });

  it('should export button style', () => {
    expect(TextStyles.button).toBeDefined();
    expect(TextStyles.button.fontSize).toBeDefined();
    expect(TextStyles.button.fontFamily).toBeDefined();
    expect(TextStyles.button.color).toBeDefined();
  });

  it('should export panelTitle style', () => {
    expect(TextStyles.panelTitle).toBeDefined();
    expect(TextStyles.panelTitle.fontSize).toBeDefined();
    expect(TextStyles.panelTitle.fontFamily).toBeDefined();
    expect(TextStyles.panelTitle.color).toBeDefined();
  });

  it('should export normal style', () => {
    expect(TextStyles.normal).toBeDefined();
    expect(TextStyles.normal.fontSize).toBeDefined();
    expect(TextStyles.normal.fontFamily).toBeDefined();
    expect(TextStyles.normal.color).toBeDefined();
  });

  it('should export small style', () => {
    expect(TextStyles.small).toBeDefined();
    expect(TextStyles.small.fontSize).toBeDefined();
    expect(TextStyles.small.fontFamily).toBeDefined();
    expect(TextStyles.small.color).toBeDefined();
  });

  it('should export resource style', () => {
    expect(TextStyles.resource).toBeDefined();
    expect(TextStyles.resource.fontSize).toBeDefined();
    expect(TextStyles.resource.fontFamily).toBeDefined();
    expect(TextStyles.resource.color).toBeDefined();
  });

  it('should export alert style', () => {
    expect(TextStyles.alert).toBeDefined();
    expect(TextStyles.alert.fontSize).toBeDefined();
    expect(TextStyles.alert.fontFamily).toBeDefined();
    expect(TextStyles.alert.color).toBeDefined();
  });

  it('should have consistent font families across styles', () => {
    const fontFamily = TextStyles.title.fontFamily;
    expect(TextStyles.subtitle.fontFamily).toBe(fontFamily);
    expect(TextStyles.button.fontFamily).toBe(fontFamily);
    expect(TextStyles.panelTitle.fontFamily).toBe(fontFamily);
    expect(TextStyles.normal.fontFamily).toBe(fontFamily);
    expect(TextStyles.small.fontFamily).toBe(fontFamily);
    expect(TextStyles.resource.fontFamily).toBe(fontFamily);
    expect(TextStyles.alert.fontFamily).toBe(fontFamily);
  });

  it('should have decreasing font sizes from title to small', () => {
    // Extract font sizes and convert to numbers
    const titleSize = parseInt(TextStyles.title.fontSize as string);
    const subtitleSize = parseInt(TextStyles.subtitle.fontSize as string);
    const buttonSize = parseInt(TextStyles.button.fontSize as string);
    const panelTitleSize = parseInt(TextStyles.panelTitle.fontSize as string);
    const normalSize = parseInt(TextStyles.normal.fontSize as string);
    const smallSize = parseInt(TextStyles.small.fontSize as string);

    // Check that font sizes decrease in the expected order
    expect(titleSize).toBeGreaterThan(subtitleSize);
    expect(subtitleSize).toBeGreaterThan(buttonSize);
    expect(buttonSize).toBeGreaterThanOrEqual(panelTitleSize);
    expect(panelTitleSize).toBeGreaterThanOrEqual(normalSize);
    expect(normalSize).toBeGreaterThan(smallSize);
  });
});
