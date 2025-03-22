import Phaser from 'phaser';

export interface PhaserTableColumn {
    header: string;
    key: string;
    width: number;
    formatter?: (value: any) => string;
}

export interface PhaserTableConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    columns: PhaserTableColumn[];
    data: any[];
    cellHeight: number;
    headerHeight?: number;
    backgroundColor?: number;
    headerBackgroundColor?: number;
    textColor?: string;
    headerTextColor?: string;
    onRowClick?: (rowData: any, index: number) => void;
}

export class PhaserTable extends Phaser.GameObjects.Container {
    private config: PhaserTableConfig;
    private headerContainer!: Phaser.GameObjects.Container;
    private rowsContainer!: Phaser.GameObjects.Container;
    private background!: Phaser.GameObjects.Rectangle;
    private rows: Phaser.GameObjects.Container[] = [];
    private totalWidth!: number;
    private visibleRows!: number;
    private scrollPosition: number = 0;
    private maskGraphics!: Phaser.GameObjects.Graphics;
    
    constructor(config: PhaserTableConfig) {
        super(config.scene, config.x, config.y);
        this.config = {
            ...config,
            headerHeight: config.headerHeight || config.cellHeight * 1.2,
            backgroundColor: config.backgroundColor || 0x111111,
            headerBackgroundColor: config.headerBackgroundColor || 0x222222,
            textColor: config.textColor || '#FFFFFF',
            headerTextColor: config.headerTextColor || '#FFFFFF'
        };
        
        // Calculate total width
        this.totalWidth = this.config.columns.reduce((total, column) => total + column.width, 0);
        
        // Calculate number of visible rows based on scene height
        const availableHeight = this.scene.cameras.main.height - config.y - config.headerHeight!;
        this.visibleRows = Math.floor(availableHeight / config.cellHeight);
        
        // Create main components
        this.createBackground();
        this.headerContainer = this.createHeader();
        this.rowsContainer = this.createRows();
        
        // Add to container
        this.add([this.background, this.headerContainer, this.rowsContainer]);
        
        // Create mask for scrolling
        this.createMask();
        
        // Add to scene
        this.scene.add.existing(this);
        
        // Setup interaction
        this.setInteractive(new Phaser.Geom.Rectangle(
            -this.totalWidth / 2, 
            -this.config.headerHeight! / 2, 
            this.totalWidth, 
            this.config.headerHeight! + (this.visibleRows * this.config.cellHeight)
        ), Phaser.Geom.Rectangle.Contains);
        
        // Setup wheel listener
        this.setupWheelListener();
    }
    
    private createBackground(): void {
        this.background = this.scene.add.rectangle(
            0, 
            (this.config.headerHeight! + (this.visibleRows * this.config.cellHeight)) / 2 - this.config.headerHeight! / 2, 
            this.totalWidth, 
            this.config.headerHeight! + (this.visibleRows * this.config.cellHeight),
            this.config.backgroundColor
        );
        this.background.setStrokeStyle(2, 0x333333);
    }
    
    private createHeader(): Phaser.GameObjects.Container {
        const container = new Phaser.GameObjects.Container(this.scene, 0, 0);
        
        // Header background
        const headerBg = this.scene.add.rectangle(
            0, 
            0, 
            this.totalWidth, 
            this.config.headerHeight!,
            this.config.headerBackgroundColor
        );
        headerBg.setOrigin(0.5, 0.5);
        container.add(headerBg);
        
        // Header cells
        let xPos = -this.totalWidth / 2 + this.config.columns[0].width / 2;
        this.config.columns.forEach(column => {
            // Add separator line except for first column
            if (xPos > -this.totalWidth / 2 + this.config.columns[0].width / 2) {
                const line = this.scene.add.line(
                    xPos - column.width / 2, 
                    0,
                    0, 0,  // Start at y=0 instead of negative
                    0, this.config.headerHeight!,
                    0x444444
                );
                container.add(line);
            }
            
            // Add header text
            const headerText = this.scene.add.text(
                xPos, 
                0, 
                column.header, 
                { 
                    fontFamily: 'monospace', 
                    fontSize: '16px', 
                    color: this.config.headerTextColor,
                    align: 'center'
                }
            );
            headerText.setOrigin(0.5);

            // Set fixed width to ensure center alignment
            headerText.setFixedSize(column.width - 20, 0);
            
            container.add(headerText);
            
            // Move to next column position
            xPos += column.width;
        });
        
        return container;
    }
    
    private createRows(): Phaser.GameObjects.Container {
        const container = new Phaser.GameObjects.Container(
            this.scene, 
            0, 
            this.config.headerHeight! / 2
        );
        
        // Create visible rows
        for (let i = 0; i < Math.min(this.visibleRows, this.config.data.length); i++) {
            const rowContainer = this.createRow(i);
            rowContainer.y = i * this.config.cellHeight;
            container.add(rowContainer);
            this.rows.push(rowContainer);
        }
        
        return container;
    }
    
    private createRow(dataIndex: number): Phaser.GameObjects.Container {
        const rowData = this.config.data[dataIndex];
        const rowContainer = new Phaser.GameObjects.Container(this.scene, 0, 0);
        
        // Row background (alternating colors)
        const bgColor = dataIndex % 2 === 0 ? 0x111111 : 0x181818;
        const rowBg = this.scene.add.rectangle(
            0, 
            0, 
            this.totalWidth, 
            this.config.cellHeight,
            bgColor
        );
        rowBg.setOrigin(0.5, 0);
        rowContainer.add(rowBg);
        
        // Make the row interactive
        rowBg.setInteractive()
            .on('pointerover', () => {
                rowBg.setFillStyle(0x222222);
            })
            .on('pointerout', () => {
                rowBg.setFillStyle(bgColor);
            })
            .on('pointerdown', () => {
                if (this.config.onRowClick) {
                    this.config.onRowClick(rowData, dataIndex);
                }
            });
        
        // Row cells
        let xPos = -this.totalWidth / 2 + this.config.columns[0].width / 2;
        this.config.columns.forEach(column => {
            const value = rowData[column.key];
            
            if (value instanceof Phaser.GameObjects.Container) {
                // If the value is a container, add it directly
                value.setPosition(xPos, this.config.cellHeight / 2);
                rowContainer.add(value);
            } else {
                // For text values, create a text object
                const displayValue = column.formatter ? column.formatter(value) : String(value);
                
                const cellText = this.scene.add.text(
                    xPos, 
                    this.config.cellHeight / 2, 
                    displayValue, 
                    { 
                        fontFamily: 'monospace', 
                        fontSize: '14px', 
                        color: this.config.textColor,
                        align: 'center'
                    }
                );
                cellText.setOrigin(0.5);
                
                // Truncate text if too long
                if (cellText.width > column.width - 20) {
                    cellText.setText(displayValue.substring(0, 10) + '...');
                }
                
                rowContainer.add(cellText);
            }
            
            // Move to next column position
            xPos += column.width;
        });
        
        // Add separator line at bottom
        const separator = this.scene.add.line(
            0,
            this.config.cellHeight,
            -this.totalWidth / 2,
            0,
            this.totalWidth / 2,
            0,
            0x333333
        );
        rowContainer.add(separator);
        
        // Store data index on the container for reference
        (rowContainer as any).dataIndex = dataIndex;
        
        return rowContainer;
    }
    
    private createMask(): void {
        // Create mask to clip rows
        this.maskGraphics = this.scene.make.graphics({});
        this.maskGraphics.fillRect(
            this.x - this.totalWidth / 2,
            this.y + this.config.headerHeight! / 2,
            this.totalWidth,
            this.visibleRows * this.config.cellHeight
        );
        
        const mask = this.maskGraphics.createGeometryMask();
        this.rowsContainer.setMask(mask);
    }
    
    public scroll(direction: number): void {
        const maxScroll = Math.max(0, this.config.data.length - this.visibleRows);
        
        // Update scroll position
        this.scrollPosition = Phaser.Math.Clamp(
            this.scrollPosition + direction,
            0,
            maxScroll
        );
        
        // Update visible rows
        this.updateVisibleRows();
    }
    
    private updateVisibleRows(): void {
        // Update each row with new data
        this.rows.forEach((row, index) => {
            const dataIndex = this.scrollPosition + index;
            
            if (dataIndex < this.config.data.length) {
                // Update row data
                const rowData = this.config.data[dataIndex];
                (row as any).dataIndex = dataIndex;
                
                // Update cell texts
                let cellIndex = 0;
                this.config.columns.forEach(column => {
                    const value = rowData[column.key];
                    const displayValue = column.formatter ? column.formatter(value) : String(value);
                    
                    // Find the text object (skip background and separator)
                    const cellText = row.getAt(cellIndex + 1) as Phaser.GameObjects.Text;
                    if (cellText && cellText instanceof Phaser.GameObjects.Text) {
                        cellText.setText(displayValue);
                        
                        // Truncate if needed
                        if (cellText.width > column.width - 20) {
                            cellText.setText(displayValue.substring(0, 10) + '...');
                        }
                    }
                    
                    cellIndex++;
                });
                
                // Show the row
                row.setVisible(true);
            } else {
                // Hide row if no data
                row.setVisible(false);
            }
        });
    }
    
    public updateData(newData: any[]): void {
        this.config.data = newData;
        this.scrollPosition = 0;
        this.updateVisibleRows();
    }

    private setupWheelListener(): void {
        // Setup mouse wheel scrolling
        this.scene.input.on('wheel', (pointer: Phaser.Input.Pointer, gameObjects: Phaser.GameObjects.GameObject[], deltaX: number, deltaY: number) => {
            if ((gameObjects as any[]).includes(this)) {
                this.scroll(deltaY > 0 ? 1 : -1);
            }
        });
    }

    public destroy(fromScene?: boolean): void {
        // Clean up event listeners if scene exists and is active
        if (this.scene && this.scene.sys.isActive() && this.scene.input) {
            this.scene.input.off('wheel');
        }
        
        // Clean up mask
        if (this.maskGraphics) {
            this.maskGraphics.destroy();
        }
        
        // Clean up rows
        this.rows.forEach(row => row.destroy());
        this.rows = [];
        
        // Call parent destroy
        super.destroy(fromScene);
    }
}