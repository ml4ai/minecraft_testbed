export class BlobBuilder {
  private readonly parts: string[];
  private blob: Blob;

  constructor() {
    this.parts = [];
  }

  prepend(part: any): void {
    this.parts.unshift(part);
    this.blob = undefined; // Invalidate the blob
  }

  append(part: any): void {
    this.parts.push(part);
    this.blob = undefined; // Invalidate the blob
  }

  getBlob(): Blob {
    if (!this.blob) {
      //The problem is that the array [1,2,3] is turned into a string "1,2,3". You can see this by running String([1,2,3]) in your browser console.
      //
      // To get around this, try:
      //
      // let newFile = new Blob([result['list'].join('\n')], {type: "text/plain", endings: 'native'});
      this.blob = new Blob([this.parts.join('\n')], {type: "text/plain", endings: 'native'});
    }
    return this.blob;
  }

  getLength(): number {
    return this.parts.length;
  }
}
