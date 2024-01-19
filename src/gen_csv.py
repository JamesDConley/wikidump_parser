import xml.etree.ElementTree as ET
from tqdm import tqdm
import csv

def process_xml(xml_path=, outpath="wikipedia_dump.csv")
    # Open the XML file using the iterparse method
    context = ET.iterparse(xml_path, events=('start', 'end'))

    # Get the root element
    _, root = next(context)

   
    with open('wikipedia_dump.csv', 'w', encoding='utf-8', newline='') as csv_file:
        # Write the csv header
        writer = csv.writer(csv_file)
        writer.writerow(['Article Name', 'Article Text', 'Metadata'])

        # Loop through all the pages
        for event, elem in tqdm(context):
            if event == 'end' and elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                # Get the title of the article
                title = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title').text

                # Get the article wikitext
                text = elem.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text').text

                # Get basic article metadata
                metadata = ''
                metadata += 'Timestamp: ' + elem.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}timestamp').text

                # Write the row to the CSV file
                writer.writerow([title, text, metadata])

                # Clear the element from memory
                root.clear()
if __name__ == "__main__":
    # Get the events from the command-line arguments
    parser = argparse.ArgumentParser(description='Given a wikipedia dump in xml format, parse articles and write to csv')
    parser.add_argument('-i', '--input-file', type=str, help='Path to the wikipedia dump xml file', default='enwiki-20230301-pages-articles-multistream.xml')
    parser.add_argument('-o', '--output-file', type=str, help='Path to the output csv file', default='wikipedia_dump.csv')

    args = parser.parse_args()
    process_xml(args.input_file, args.output_file)